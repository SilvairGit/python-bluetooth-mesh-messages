#
# python-bluetooth-mesh - Bluetooth Mesh for Python
#
# Copyright (C) 2019  SILVAIR sp. z o.o.
#
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
"""
Unit tests for Composition Data Page 1 (Extended Model Items) parsing, per
Bluetooth Mesh Protocol v1.1, Tables 4.8-4.11.

These tests cover a regression in ``ExtendedModelLongFormat``, where
``element_offset`` and ``model_item_index`` were swapped relative to the
specification (see unittest_brief_composition_data_page1.md for the full
writeup, including the real device message used in the end-to-end test).
"""

import pytest

from bluetooth_mesh.messages.config import (
    CompositionDataPage,
    CompositionDataPage1Element,
    ConfigMessage,
    ConfigOpcode,
    ExtendedModelLongFormat,
    ExtendedModelShortFormat,
    ExtendedModelsItemFormat,
)

short_format_valid = [
    pytest.param(
        bytes.fromhex("00"),
        {"model_item_index": 0, "element_offset": 0},
        id="short - index min, offset 0",
    ),
    pytest.param(
        bytes.fromhex("FB"),
        {"model_item_index": 31, "element_offset": 3},
        id="short - index max, offset max positive",
    ),
    pytest.param(
        bytes.fromhex("07"),
        {"model_item_index": 0, "element_offset": -1},
        id="short - index min, offset -1",
    ),
    pytest.param(
        bytes.fromhex("FC"),
        {"model_item_index": 31, "element_offset": -4},
        id="short - index max, offset min negative",
    ),
]

long_format_valid = [
    pytest.param(
        bytes.fromhex("0020"),
        {"element_offset": 0, "model_item_index": 32},
        id="long - regression case (Element 1, vendor idx 11 from real message)",
    ),
    pytest.param(
        bytes.fromhex("FFFF"),
        {"element_offset": -1, "model_item_index": 255},
        id="long - offset -1, index max",
    ),
    pytest.param(
        bytes.fromhex("7F00"),
        {"element_offset": 127, "model_item_index": 0},
        id="long - offset max positive, index min",
    ),
    pytest.param(
        bytes.fromhex("8000"),
        {"element_offset": -128, "model_item_index": 0},
        id="long - offset min negative, index min",
    ),
]


@pytest.mark.parametrize("encoded,decoded", short_format_valid)
def test_extended_model_short_format_parse(encoded, decoded):
    assert ExtendedModelShortFormat.parse(encoded) == decoded


@pytest.mark.parametrize("encoded,decoded", short_format_valid)
def test_extended_model_short_format_build(encoded, decoded):
    assert ExtendedModelShortFormat.build(decoded) == encoded


@pytest.mark.parametrize("encoded,decoded", long_format_valid)
def test_extended_model_long_format_parse(encoded, decoded):
    assert ExtendedModelLongFormat.parse(encoded) == decoded


@pytest.mark.parametrize("encoded,decoded", long_format_valid)
def test_extended_model_long_format_build(encoded, decoded):
    assert ExtendedModelLongFormat.build(decoded) == encoded


# Element with a mix of Model Items:
#   sig_models[0]:    root model, no extensions
#   sig_models[1]:    model with a corresponding_id
#   vendor_models[0]: model with one short-format Extended Model Item
#   vendor_models[1]: model with one long-format Extended Model Item
#                      (bytes "06 00 20" - the long-format regression case)
COMPOSITION_DATA_PAGE1_ELEMENT_ENCODED = bytes.fromhex("0202000105042F060020")

COMPOSITION_DATA_PAGE1_ELEMENT_DECODED = {
    "number_s": 2,
    "number_v": 2,
    "sig_models": [
        {
            "extended_items_count": 0,
            "format": ExtendedModelsItemFormat.SHORT,
            "corresponding_present": False,
            "corresponding_id": 0,
            "extended_models_items": {"short": []},
        },
        {
            "extended_items_count": 0,
            "format": ExtendedModelsItemFormat.SHORT,
            "corresponding_present": True,
            "corresponding_id": 0x05,
            "extended_models_items": {"short": []},
        },
    ],
    "vendor_models": [
        {
            "extended_items_count": 1,
            "format": ExtendedModelsItemFormat.SHORT,
            "corresponding_present": False,
            "corresponding_id": 0,
            "extended_models_items": {"short": [{"model_item_index": 5, "element_offset": -1}]},
        },
        {
            "extended_items_count": 1,
            "format": ExtendedModelsItemFormat.LONG,
            "corresponding_present": False,
            "corresponding_id": 0,
            "extended_models_items": {"long": [{"element_offset": 0, "model_item_index": 32}]},
        },
    ],
}


def test_composition_data_page1_element_parse():
    result = CompositionDataPage1Element.parse(COMPOSITION_DATA_PAGE1_ELEMENT_ENCODED)
    assert result == COMPOSITION_DATA_PAGE1_ELEMENT_DECODED


def test_composition_data_page1_element_build():
    result = CompositionDataPage1Element.build(COMPOSITION_DATA_PAGE1_ELEMENT_DECODED)
    assert result == COMPOSITION_DATA_PAGE1_ELEMENT_ENCODED


# Real CONFIG_COMPOSITION_DATA_STATUS message for Page 1, captured from a device
# log. It is the only message with a long-format Extended Model Item on this
# device (Element 1, vendor model index 11), which is exactly the entry that
# the ExtendedModelLongFormat field-order bug corrupted.
CONFIG_COMPOSITION_DATA_STATUS_PAGE1_HEX = (
    "02"  # opcode: CONFIG_COMPOSITION_DATA_STATUS
    "01"  # page: 1
    "160D00000000000000050210090238300001090509500100010001010901703001"
    "060906803009033820090390400508900908A0980000000000010B050BD8000460"
    "0000060020000701000000010A050A180904970005042805043001020009059600"
    "0505080701000000010709071810000508080C280010"
)


def test_config_composition_data_status_page1_end_to_end():
    encoded = bytes.fromhex(CONFIG_COMPOSITION_DATA_STATUS_PAGE1_HEX)

    msg = ConfigMessage.parse(encoded)

    assert msg["opcode"] == ConfigOpcode.CONFIG_COMPOSITION_DATA_STATUS
    assert msg["params"]["page"] == CompositionDataPage.FIRST

    elements = msg["params"]["data"]["element"]
    assert len(elements) == 4

    expected_counts = [
        (22, 13),
        (7, 1),
        (1, 2),
        (7, 1),
    ]
    for element, (number_sig_models, number_vendor_models) in zip(elements, expected_counts):
        assert element["number_s"] == number_sig_models
        assert element["number_v"] == number_vendor_models

    long_format_item = elements[0]["vendor_models"][11]
    assert long_format_item["format"] == ExtendedModelsItemFormat.LONG
    long_items = long_format_item["extended_models_items"]["long"]
    assert len(long_items) == 1
    assert long_items[0]["element_offset"] == 0
    assert long_items[0]["model_item_index"] == 32

    assert ConfigMessage.build(msg) == encoded
