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
from datetime import timedelta

import pytest

from bluetooth_mesh.messages.silvair.light_extended_controller import (
    LightExtendedControllerMessage,
    LightExtendedControllerOpcode,
    LightExtendedControllerProperty,
    LightExtendedControllerSubOpcode,
)

valid = [
    # fmt: off
    pytest.param(
        bytes.fromhex("f636010071ff"),
        LightExtendedControllerOpcode.SILVAIR_LEC,
        dict(
            subopcode=LightExtendedControllerSubOpcode.PROPERTY_GET,
            payload=dict(
                property_id=LightExtendedControllerProperty.AUTO_RESUME_MODE,
            )
        ),
        id="LIGHT_LEC_PROPERTY_GET[AUTO_RESUME_MODE]"
    ),
    pytest.param(
        bytes.fromhex("f636010171ff01"),
        LightExtendedControllerOpcode.SILVAIR_LEC,
        dict(
            subopcode=LightExtendedControllerSubOpcode.PROPERTY_SET,
            payload=dict(
                property_id=LightExtendedControllerProperty.AUTO_RESUME_MODE,
                auto_resume_mode=True,
            )
        ),
        id="LIGHT_LEC_PROPERTY_SET[AUTO_RESUME_MODE]"
    ),
    pytest.param(
        bytes.fromhex("f636010272ff10A400"),
        LightExtendedControllerOpcode.SILVAIR_LEC,
        dict(
            subopcode=LightExtendedControllerSubOpcode.PROPERTY_SET_UNACKNOWLEDGED,
            payload=dict(
                property_id=LightExtendedControllerProperty.AUTO_RESUME_TIMER,
                auto_resume_timer=dict(seconds=42),
            )
        ),
        id="LIGHT_LEC_PROPERTY_SET_UNACKNOWLEDGED[AUTO_RESUME_TIMER]"
    ),
    pytest.param(
        bytes.fromhex("f636010372ff90ca04"),
        LightExtendedControllerOpcode.SILVAIR_LEC,
        dict(
            subopcode=LightExtendedControllerSubOpcode.PROPERTY_STATUS,
            payload=dict(
                property_id=LightExtendedControllerProperty.AUTO_RESUME_TIMER,
                auto_resume_timer=dict(seconds=314),
            )
        ),
        id="LIGHT_LEC_PROPERTY_STATUS[AUTO_RESUME_TIMER]"
    ),
    # fmt: on
]


@pytest.mark.parametrize("encoded,opcode,data", valid)
def test_parse_valid(encoded, opcode, data):
    LightExtendedControllerMessage.parse(encoded).params == data


@pytest.mark.parametrize("encoded,opcode,data", valid)
def test_build_valid(encoded, opcode, data):
    assert LightExtendedControllerMessage.build(dict(opcode=opcode, params=data)) == encoded
