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
import importlib
import json
import logging
from tempfile import NamedTemporaryFile

import pytest

from bluetooth_mesh.messages import AccessMessage
from bluetooth_mesh.messages.util import to_camelcase_dict, to_snakecase_dict

valid = [
    # Silvair Debug Server
    bytes.fromhex("F53601" + "00"),  # RSSI_THRESHOLD_GET
    bytes.fromhex("F53601" + "01" + "f0"),  # RSSI_THRESHOLD_SET
    bytes.fromhex("F53601" + "02" + "f0"),  # RSSI_THRESHOLD_STATUS
    bytes.fromhex("F53601" + "03" + "ff"),  # RADIO_TEST
    bytes.fromhex("F53601" + "0a"),  # UPTIME_GET
    bytes.fromhex("F53601" + "0b" + "00000000"),  # UPTIME_STATUS
    bytes.fromhex("F53601" + "0b" + "ffffffff"),  # UPTIME_STATUS
    bytes.fromhex("F53601" + "0c"),  # LAST_SW_FAULT_GET
    bytes.fromhex("F53601" + "0d"),  # LAST_SW_FAULT_CLEAR
    bytes.fromhex("F53601" + "0e" + "00000000" + "616263"),  # LAST_SW_FAULT_STATUS
    bytes.fromhex("F53601" + "0f"),  # SYSTEM_STATS_GET
    bytes.fromhex("F53601" + "10"),  # SYSTEM_STATS_STATUS
    bytes.fromhex("F53601" + "10" + "6162636465666768000000000000"),
    bytes.fromhex("F53601" + "10" + "6162636400000000ffff00000000"),
    bytes.fromhex("F53601" + "11"),  # LAST_MALLOC_FAULT_GET
    bytes.fromhex("F53601" + "12"),  # LAST_MALLOC_FAULT_CLEAR
    bytes.fromhex("F53601" + "13" + "00000000" + "616263"),  # LAST_MALLOC_FAULT_STATUS
    bytes.fromhex("F53601" + "14"),  # LAST_FDS_FAULT_GET
    bytes.fromhex("F53601" + "15"),  # LAST_FDS_FAULT_CLEAR
    bytes.fromhex("F53601" + "16" + "00000000" + "616263"),  # LAST_FDS_FAULT_STATUS
    bytes.fromhex("F53601" + "17"),  # BYTES_BEFORE_GARBAGE_COLLECTOR_GET
    bytes.fromhex("F53601" + "18" + "0000"),  # BYTES_BEFORE_GARBAGE_COLLECTOR_STATUS
    bytes.fromhex("F53601" + "18" + "1234"),  # BYTES_BEFORE_GARBAGE_COLLECTOR_STATUS
    bytes.fromhex("F53601" + "18" + "ffff"),  # BYTES_BEFORE_GARBAGE_COLLECTOR_STATUS
    bytes.fromhex("F53601" + "19"),  # PROVISIONED_APP_VERSION_GET
    bytes.fromhex("F53601" + "1a" + "0000"),  # PROVISIONED_APP_VERSION_STATUS
    bytes.fromhex("F53601" + "1a" + "1234"),  # PROVISIONED_APP_VERSION_STATUS
    bytes.fromhex("F53601" + "1a" + "ffff"),  # PROVISIONED_APP_VERSION_STATUS
    bytes.fromhex("F53601" + "1b"),  # FULL_FIRMWARE_VERSION_GET
    bytes.fromhex("F53601" + "1c" + "61626364"),  # FULL_FIRMWARE_VERSION_STATUS
    bytes.fromhex("F53601" + "1d"),  # IV_INDEX_GET
    bytes.fromhex("F53601" + "1e" + "00000000"),  # IV_INDEX_STATUS
    bytes.fromhex("F53601" + "1e" + "12345678"),  # IV_INDEX_STATUS
    bytes.fromhex("F53601" + "1e" + "ffffffff"),  # IV_INDEX_STATUS
    bytes.fromhex("F53601" + "1f"),  # GARBAGE_COLLECTOR_COUNTER_GET
    bytes.fromhex("F53601" + "20" + "0000"),  # GARBAGE_COLLECTOR_COUNTER_STATUS
    bytes.fromhex("F53601" + "20" + "1234"),  # GARBAGE_COLLECTOR_COUNTER_STATUS
    bytes.fromhex("F53601" + "20" + "ffff"),  # GARBAGE_COLLECTOR_COUNTER_STATUS
    bytes.fromhex("F53601" + "21"),  # ARAP_LIST_SIZE_GET
    bytes.fromhex("F53601" + "22" + "0000"),  # ARAP_LIST_SIZE_STATUS
    bytes.fromhex("F53601" + "22" + "1234"),  # ARAP_LIST_SIZE_STATUS
    bytes.fromhex("F53601" + "22" + "ffff"),  # ARAP_LIST_SIZE_STATUS
    bytes.fromhex("F53601" + "22" + "00000000"),  # ARAP_LIST_SIZE_STATUS
    bytes.fromhex("F53601" + "22" + "12345678"),  # ARAP_LIST_SIZE_STATUS
    bytes.fromhex("F53601" + "22" + "ffffffff"),  # ARAP_LIST_SIZE_STATUS
    bytes.fromhex("F53601" + "23" + "00"),  # ARAP_LIST_CONTENT_GET
    bytes.fromhex("F53601" + "23" + "12"),  # ARAP_LIST_CONTENT_GET
    bytes.fromhex("F53601" + "23" + "ff"),  # ARAP_LIST_CONTENT_GET
    bytes.fromhex("F53601" + "24" + "0000"),  # ARAP_LIST_CONTENT_STATUS
    bytes.fromhex("F53601" + "24" + "00" + "00" + "0000000000"),  # ARAP_LIST_CONTENT_STATUS
    bytes.fromhex("F53601" + "24" + "00" + "00" + "ffffffffff"),  # ARAP_LIST_CONTENT_STATUS
    bytes.fromhex(
        "F53601" + "24" + "00" + "00" + "ffffffffff00000000001234561234"
    ),  # ARAP_LIST_CONTENT_STATUS
    # ------------------
    # Configuration Client
    bytes.fromhex("02" + "00" + "3601CE00FECAEFBE0BB000000000"),  # CONFIG_COMPOSITION_DATA_STATUS
    bytes.fromhex("8002" + "00" + "0b00010000012100"),  # CONFIG_APPKEY_LIST
    bytes.fromhex("8039" + "01" + "02" + "03" + "04" + "0506070809"),  # CONFIG_HEARBEAT_PUBLICATION_SET
    bytes.fromhex("803E" + "00" + "A70202000213"),  # CONFIG_MODEL_APP_STATUS
    # ------------------
    # Light CTL Server
    bytes.fromhex("8265" + "2222" + "3333" + "ff" + "32" + "3c"),  # LIGHT_CTL_TEMPERATURE_SET_UNACKNOWLEDGED
    # ------------------
    # Network Diagnostic Setup Server
    bytes.fromhex("fd3601" + "00"),  # PUBLICATION_GET
    bytes.fromhex("fd3601" + "01" + "1234aaaa82031000"),  # PUBLICATION_SET
    bytes.fromhex("fd3601" + "01" + "1234aaaa820310000300"),  # PUBLICATION_SET
    bytes.fromhex("fd3601" + "01" + "1234aaaa82031000"),  # PUBLICATION_SET
    bytes.fromhex("fd3601" + "02" + "1234aaaa820310000300"),  # PUBLICATION_STATUS
    bytes.fromhex("fc3601" + "00"),  # SUBSCRIPTION_GET
    bytes.fromhex("fc3601" + "01" + "0123aaaa"),  # SUBSCRIPTION_SET
    bytes.fromhex("fc3601" + "02" + "0123aaaa"),  # SUBSCRIPTION_SET_UNACKNOWLEDGED
    bytes.fromhex("fc3601" + "03" + "1234aaaa20012300110101"),  # SUBSCRIPTION_STATUS
    # ------------------
    # Sensor Server
    bytes.fromhex("8230"),  # SENSOR_DESCRIPTOR_GET
    bytes.fromhex("8230" + "0400"),  # SENSOR_DESCRIPTOR_GET
    bytes.fromhex("8231"),  # SENSOR_GET
    bytes.fromhex("8231" + "0700"),  # SENSOR_GET
    bytes.fromhex("51" + "0c00000000040b0c"),  # SENSOR_DESCRIPTOR_STATUS
    bytes.fromhex("51" + "1900"),  # SENSOR_DESCRIPTOR_STATUS
    bytes.fromhex("51" + "0c00000000020b0c1f00efcdab071b1c"),  # SENSOR_DESCRIPTOR_STATUS
    bytes.fromhex("52" + "e20ac800"),  # SENSOR_STATUS
    bytes.fromhex("52" + "220b2003"),  # SENSOR_STATUS
    bytes.fromhex("52" + "440da244ff"),  # SENSOR_STATUS
    bytes.fromhex("52" + "09" + "9040" + "a244" + "ff0000"),  # SENSOR_STATUS
    bytes.fromhex("52" + "44" + "0da2" + "44ff" + "220b2003"),  # SENSOR_STATUS
    bytes.fromhex("58" + "3000" + "0100" + "0400" + "0900"),  # SENSOR_SETTINGS_STATUS
    bytes.fromhex("58" + "3000"),  # SENSOR_SETTINGS_STATUS
    bytes.fromhex("59" + "5700" + "5700" + "c800"),  # SENSOR_SETTING_SET
    bytes.fromhex("5b" + "5700" + "5700" + "01" + "c800"),  # SENSOR_SETTING_STATUS
    bytes.fromhex("5b" + "5700" + "0200" + "01" + "c80039"),  # SENSOR_SETTING_STATUS
    bytes.fromhex("59" + "5700" + "5700" + "c800"),  # SENSOR_SETTING_SET
    bytes.fromhex("59" + "5700" + "0200" + "c80039"),  # SENSOR_SETTING_SET
    bytes.fromhex("59" + "0500" + "0500" + "200354"),  # SENSOR_SETTING_SET
    bytes.fromhex("59" + "5700" + "0200" + "c80000"),  # SENSOR_SETTING_SET
    bytes.fromhex("59" + "5900" + "5900" + "0003"),  # SENSOR_SETTING_SET
    bytes.fromhex("59" + "4200" + "4d00" + "01"),  # SENSOR_SETTING_SET
    bytes.fromhex("59" + "4200" + "4200" + "50"),  # SENSOR_SETTING_SET
    bytes.fromhex("59" + "0a00" + "3600" + "b80b00"),  # SENSOR_SETTING_SET
    bytes.fromhex("59" + "6d00" + "6d00" + "0a0000"),  # SENSOR_SETTING_SET
    bytes.fromhex("59" + "6d00" + "6d00" + "ffffff"),
    bytes.fromhex("59" + "550055001a2700"),  # SENSOR_SETTING_SET
    bytes.fromhex("59" + "4c004c001b1a"),  # SENSOR_SETTING_SET
    bytes.fromhex("59" + "6c006c00ff1b1a"),  # SENSOR_SETTING_SET
    bytes.fromhex("59" + "6c00" + "6c00" + "ffffff"),  # SENSOR_SETTING_SET + TOTAL_DEVICE_POWER_ON_CYCLES
    bytes.fromhex("59" + "6800" + "6800" + "0500"),  # SENSOR_SETTING_SET + TIME_SINCE_MOTION_SENSED
    bytes.fromhex(
        "59" + "6700" + "6700" + "050001007040"
    ),  # SENSOR_SETTING_SET + SHORT_CIRCUIT_EVENT_STATISTICS
    bytes.fromhex(
        "59" + "0e00" + "0e00" + "6162636465666768"
    ),  # SENSOR_SETTING_SET + DEVICE_FIRMWARE_REVISION
    bytes.fromhex(
        "59" + "0e00" + "0e00" + "6162636465660000"
    ),  # SENSOR_SETTING_SET + DEVICE_FIRMWARE_REVISION
    bytes.fromhex(
        "59" + "1100" + "1100" + "616263646566676861626364656667686162636465666768616263646566676861626364"
    ),
    # SENSOR_SETTING_SET + DEVICE_MANUFACTURER_NAME
    bytes.fromhex("59" + "6a00" + "6a00" + "a244ff"),  # SENSOR_SETTING_SET + TOTAL_DEVICE_ENERGY_USE
    bytes.fromhex("59" + "2e00" + "2e00" + "44ff"),  # SENSOR_SETTING_SET + LIGHT_CONTROL_LIGHTNESS_ON
    bytes.fromhex("59" + "3200" + "3200" + "44ff0000"),  # SENSOR_SETTING_SET + LIGHT_CONTROL_REGULATOR_KID
    bytes.fromhex("59" + "5200" + "5200" + "a08601"),  # SENSOR_SETTING_SET + PRESENT_DEVICE_INPUT_POWER
    bytes.fromhex("59" + "1600" + "1600" + "e80300d007000f2700"),
    # SENSOR_SETTING_SET + DEVICE_POWER_RANGE_SPECIFICATION
    bytes.fromhex("59" + "4f00" + "4f00" + "1f"),  # SENSOR_SETTING_SET + PRESENT_AMBIENT_TEMPERATURE
    bytes.fromhex("59" + "4f00" + "4f00" + "e1"),  # SENSOR_SETTING_SET + PRESENT_AMBIENT_TEMPERATURE
    bytes.fromhex(
        "59" + "5400" + "5400" + "e620"
    ),  # SENSOR_SETTING_SET + PRESENT_DEVICE_OPERATING_TEMPERATURE
    bytes.fromhex("59" + "4500" + "4500" + "3102dc6e71"),  # SENSOR_SETTING_SET + OUTDOOR_STATISTICAL_VALUES
    bytes.fromhex("59" + "1400" + "1400" + "92096400f8f8204e71"),
    # SENSOR_SETTING_SET + DEVICE_OPERATING_TEMPERATURE_STATISTICAL_VALUES
    bytes.fromhex("59" + "1300" + "1300" + "dc6e"),
    # SENSOR_SETTING_SET + DEVICE_OPERATING_TEMPERATURE_RANGE_SPECIFICATION
    bytes.fromhex("59" + "0100" + "0100" + "186da2"),
    # SENSOR_SETTING_SET + AVERAGE_AMBIENT_TEMPERATURE_IN_A_PERIOD_OF_DAY
    bytes.fromhex("59" + "6000" + "6000" + "a244ff6da2"),
    # SENSOR_SETTING_SET + RELATIVE_DEVICE_ENERGY_USE_IN_A_PERIOD_OF_DAY
    bytes.fromhex(
        "59" + "2a00" + "2a00" + "690140000000f0ff54"
    ),  # SENSOR_SETTING_SET + INPUT_VOLTAGE_STATISTICS
    bytes.fromhex("59" + "4900" + "4900" + "00000006f0ff"),  # SENSOR_SETTING_SET + OUTPUT_VOLTAGE_RANGE
    bytes.fromhex(
        "59" + "4700" + "4700" + "9709640000007d1571"
    ),  # SENSOR_SETTING_SET + OUTPUT_CURRENT_STATISTICS
    bytes.fromhex("59" + "4600" + "4600" + "00007d15"),  # SENSOR_SETTING_SET + OUTPUT_CURRENT_RANGE
    bytes.fromhex(
        "59" + "2100" + "2100" + "000001007d15"
    ),  # SENSOR_SETTING_SET + INPUT_CURRENT_RANGE_SPECIFICATION
    bytes.fromhex("59" + "7000" + "7000" + "020000"),  # SENSOR_SETTING_SET + TOTAL_LUMINOUS_ENERGY
    bytes.fromhex(
        "59" + "0600" + "0600" + "0020"
    ),  # SENSOR_SETTING_SET + CENTER_BEAM_INTENSITY_AT_FULL_POWER
    bytes.fromhex("59" + "4000" + "4000" + "020000"),  # SENSOR_SETTING_SET + LUMINOUS_EXPOSURE
    bytes.fromhex("59" + "1f00" + "1f00" + "d007"),  # SENSOR_SETTING_SET + INITIAL_LUMINOUS_FLUX
    bytes.fromhex("59" + "4100" + "4100" + "e803d007"),  # SENSOR_SETTING_SET + LUMINOUS_FLUX_RANGE
    bytes.fromhex("59" + "3e00" + "3e00" + "d407"),  # SENSOR_SETTING_SET + LUMINOUS_EFFICACY
    bytes.fromhex(
        "59" + "0f00" + "0f00" + "ffeeddccbbaa"
    ),  # SENSOR_SETTING_SET + DEVICE_GLOBAL_TRADE_ITEM_NUMBER
    bytes.fromhex("59" + "0700" + "0700" + "64"),  # SENSOR_SETTING_SET + CHROMATICITY_TOLERANCE
    bytes.fromhex("59" + "5e00" + "5e00" + "9227"),  # SENSOR_SETTING_SET + PRESENT_PLANCKIAN_DISTANCE
    bytes.fromhex(
        "59" + "5100" + "5100" + "b80b"
    ),  # SENSOR_SETTING_SET + PRESENT_CORRELATED_COLOR_TEMPERATURE
    bytes.fromhex("59" + "0a00" + "0a00" + "04f0"),  # SENSOR_SETTING_SET + DEVICE_APPEARANCE
    bytes.fromhex("59" + "0b00" + "0b00" + "2a00"),  # SENSOR_SETTING_SET + DEVICE_COUNTRY_OF_ORIGIN
    bytes.fromhex("59" + "0c00" + "0c00" + "de4600"),  # SENSOR_SETTING_SET + DEVICE_DATE_OF_MANUFACTURE
    bytes.fromhex(
        "59" + "5000" + "5000" + "ee00cdab"
    ),  # SENSOR_SETTING_SET + PRESENT_CIE1931_CHROMATICITY_COORDINATES
    bytes.fromhex("59" + "0800" + "0800" + "64"),  # SENSOR_SETTING_SET + COLOR_RENDERING_INDEX_R9
    bytes.fromhex("59" + "0800" + "0800" + "9c"),  # SENSOR_SETTING_SET + COLOR_RENDERING_INDEX_R9
    bytes.fromhex("59" + "6100" + "6100" + "88aa00bbbb"),
    # SENSOR_SETTING_SET + RELATIVE_DEVICE_RUNTIME_IN_A_GENERIC_LEVEL_RANGE
    bytes.fromhex("59" + "6200" + "6200" + "881a27001a2700"),
    # SENSOR_SETTING_SET + RELATIVE_EXPOSURE_TIME_IN_AN_ILLUMINANCE_RANGE
    bytes.fromhex("59" + "6400" + "6400" + "88ffffe620"),
    # SENSOR_SETTING_SET + RELATIVE_RUNTIME_IN_A_DEVICE_OPERATING_TEMPERATURE_RANGE
    bytes.fromhex("59" + "6500" + "6500" + "880000cdab"),
    # SENSOR_SETTING_SET + RELATIVE_RUNTIME_IN_AN_INPUT_CURRENT_RANGE
    bytes.fromhex("59" + "6600" + "6600" + "8820032003"),
    # SENSOR_SETTING_SET + RELATIVE_RUNTIME_IN_AN_INPUT_VOLTAGE_RANGE
    # ------------------
    # Light Lightness Server
    bytes.fromhex("824b"),  # LIGHT_LIGHTNESS_GET
    bytes.fromhex("824c" + "bbaa22"),  # LIGHT_LIGHTNESS_SET
    bytes.fromhex("824c" + "010022"),  # LIGHT_LIGHTNESS_SET
    bytes.fromhex("824c" + "000031323c"),  # LIGHT_LIGHTNESS_SET
    bytes.fromhex("824d" + "000031323c"),  # LIGHT_LIGHTNESS_SET_UNACKNOWLEDGED
    bytes.fromhex("824e" + "4400"),  # LIGHT_LIGHTNESS_STATUS
    bytes.fromhex("824e" + "000031c80f"),  # LIGHT_LIGHTNESS_STATUS
    bytes.fromhex("824f"),  # LIGHT_LIGHTNESS_LINEAR_GET
    bytes.fromhex("8250" + "bbaa01"),  # LIGHT_LIGHTNESS_LINEAR_SET
    bytes.fromhex("8250" + "010022"),  # LIGHT_LIGHTNESS_LINEAR_SET
    bytes.fromhex("8250" + "000031321b"),  # LIGHT_LIGHTNESS_LINEAR_SET
    bytes.fromhex("8251" + "ff0031323c"),  # LIGHT_LIGHTNESS_LINEAR_SET_UNACKNOWLEDGED
    bytes.fromhex("8252" + "0000ddbb4c"),  # LIGHT_LIGHTNESS_LINEAR_STATUS
    bytes.fromhex("8253"),  # LIGHT_LIGHTNESS_LAST_GET
    bytes.fromhex("8254" + "0000"),  # LIGHT_LIGHTNESS_LAST_STATUS
    bytes.fromhex("8255"),  # LIGHT_LIGHTNESS_DEFAULT_GET
    bytes.fromhex("8256" + "0000"),  # LIGHT_LIGHTNESS_DEFAULT_STATUS
    bytes.fromhex("8257"),  # LIGHT_LIGHTNESS_RANGE_GET
    bytes.fromhex("8258" + "0011118888"),  # LIGHT_LIGHTNESS_RANGE_STATUS
    # ------------------
    # Scene Server
    bytes.fromhex("8241"),  # SCENE_GET
    bytes.fromhex("8242" + "01001e"),  # SCENE_RECALL
    bytes.fromhex("8243" + "01001e"),  # SCENE_RECALL_UNACKNOWLEDGED
    bytes.fromhex("8242" + "01001ef23c"),  # SCENE_RECALL
    bytes.fromhex("8243" + "01001ef23c"),  # SCENE_RECALL_UNACKNOWLEDGED
    bytes.fromhex("5e" + "000100"),  # SCENE_STATUS
    bytes.fromhex("5e" + "0001000200f2"),  # SCENE_STATUS
    bytes.fromhex("8244"),  # SCENE_REGISTER_GET
    bytes.fromhex("8245" + "00010001000200") + 14 * bytes.fromhex("0000"),  # SCENE_REGISTER_STATUS
    bytes.fromhex("8246" + "0100"),  # SCENE_STORE
    bytes.fromhex("8247" + "0100"),  # SCENE_STORE_UNACKNOWLEDGED
    bytes.fromhex("829e" + "0100"),  # SCENE_DELETE
    bytes.fromhex("829f" + "0100"),  # SCENE_DELETE_UNACKNOWLEDGED
    # ------------------
    # Generic OnOff Server
    bytes.fromhex("8201"),  # GENERIC_ONOFF_GET
    bytes.fromhex("8202" + "0122"),  # GENERIC_ONOFF_SET
    bytes.fromhex("8202" + "0122"),  # GENERIC_ONOFF_SET
    bytes.fromhex("8202" + "0031323c"),  # GENERIC_ONOFF_SET
    bytes.fromhex("8202" + "0031f23c"),  # GENERIC_ONOFF_SET
    bytes.fromhex("8204" + "00"),  # GENERIC_ONOFF_STATUS
    bytes.fromhex("8204" + "00014a"),  # GENERIC_ONOFF_STATUS
    bytes.fromhex("8204" + "0001ff"),  # GENERIC_ONOFF_STATUS
    # ------------------
    # Generic Level Server
    bytes.fromhex("8205"),  # GENERIC_LEVEL_GET
    bytes.fromhex("8206" + "ff7f22"),  # GENERIC_LEVEL_SET
    bytes.fromhex("8206" + "008022"),  # GENERIC_LEVEL_SET
    bytes.fromhex("8206" + "010022"),  # GENERIC_LEVEL_SET
    bytes.fromhex("8206" + "000031323c"),  # GENERIC_LEVEL_SET
    bytes.fromhex("8207" + "000031323c"),  # GENERIC_LEVEL_SET_UNACKNOWLEDGED
    bytes.fromhex("8208" + "ff7f"),  # GENERIC_LEVEL_STATUS
    bytes.fromhex("8208" + "0080"),  # GENERIC_LEVEL_STATUS
    bytes.fromhex("8208" + "0000ff004a"),  # GENERIC_LEVEL_STATUS
    bytes.fromhex("8208" + "00000100ff"),  # GENERIC_LEVEL_STATUS
    bytes.fromhex("8209" + "ffffff7f22"),  # GENERIC_DELTA_SET
    bytes.fromhex("8209" + "0000008022"),  # GENERIC_DELTA_SET
    bytes.fromhex("8209" + "0100000022"),  # GENERIC_DELTA_SET
    bytes.fromhex("8209" + "0000000031323c"),  # GENERIC_DELTA_SET
    bytes.fromhex("820a" + "0000000031323c"),  # GENERIC_DELTA_SET_UNACKNOWLEDGED
    bytes.fromhex("820b" + "ff7f22"),  # GENERIC_MOVE_SET
    bytes.fromhex("820b" + "008022"),  # GENERIC_MOVE_SET
    bytes.fromhex("820b" + "010022"),  # GENERIC_MOVE_SET
    bytes.fromhex("820b" + "000031323c"),  # GENERIC_MOVE_SET
    bytes.fromhex("820c" + "000031323c"),  # GENERIC_MOVE_SET_UNACKNOWLEDGED
    # ------------------
    # Time Server
    bytes.fromhex("5d" + "8ea9282a005905490248"),  # TIME_STATUS
    # ------------------
    # Silvair Debug Server V2
    bytes.fromhex("EB3601" + "02" + "090002001020300208000420"),  # STATUS
    bytes.fromhex("EB3601" + "02" + "0b020c06001000200030"),  # STATUS
    bytes.fromhex("EB3601" + "02" + "4b000b096d7920737472696e67"),  # STATUS
    bytes.fromhex("EB3601" + "02" + "550002001020300a000800320028"),  # STATUS
    bytes.fromhex("EB3601" + "03" + "1300"),  # CLEAR
    bytes.fromhex("EB3601" + "00" + "0f00"),  # GET
    bytes.fromhex("EB3601" + "02" + "fe00ff"),  # STATUS
    # Configuration Client
    bytes.fromhex("02" + "01" + "010000"),  # CONFIG_COMPOSITION_DATA_STATUS
    bytes.fromhex("02" + "01" + "01000400"),  # CONFIG_COMPOSITION_DATA_STATUS
    bytes.fromhex("02" + "01" + "02010005000000010201000501170101"),  # CONFIG_COMPOSITION_DATA_STATUS
    bytes.fromhex(
        "02" + "01" + "050307011AFD0901383001080508480000050A00050AD0"
    ),  # CONFIG_COMPOSITION_DATA_STATUS
    bytes.fromhex("8028" + "0200"),  # CONFIG_RELAY_STATUS
    bytes.fromhex("8028" + "02FF"),  # CONFIG_RELAY_STATUS
    bytes.fromhex("8028" + "0100"),  # CONFIG_RELAY_STATUS
    bytes.fromhex("8028" + "0000"),  # CONFIG_RELAY_STATUS
    bytes.fromhex("8028" + "01FF"),  # CONFIG_RELAY_STATUS
    bytes.fromhex("8028" + "00FF"),  # CONFIG_RELAY_STATUS
    bytes.fromhex("8027" + "0100"),  # CONFIG_RELAY_SET
    bytes.fromhex("8027" + "0000"),  # CONFIG_RELAY_SET
    bytes.fromhex("8027" + "01FF"),  # CONFIG_RELAY_SET
    bytes.fromhex("8027" + "00FF"),  # CONFIG_RELAY_SET
    # ------------------
    # Generic User Property Server
    bytes.fromhex("822E"),  # Generic User Properties Get
    bytes.fromhex(
        "4B"
        + "7300"
        + "8800"
        + "8900"
        + "8C00"
        + "8D00"
        + "8E00"
        + "8F00"
        + "9000"
        + "9100"
        + "9200"
        + "9300"
        + "9400"
        + "9500"
        + "9600"
    ),  # Generic User Properties Status
    bytes.fromhex("822F" + "6F00"),  # Generic User Property Get + Total Light Exposure Time
    bytes.fromhex("4C" + "8C00" + "03"),  # Generic User Property Set + Light Distribution + Type_III
    bytes.fromhex(
        "4D" + "8800" + "FEFFFF"
    ),  # Generic User Property Set Unacknowledged + External Supply Voltage + 262143.97 V
    bytes.fromhex(
        "4E" + "8900" + "01" + "FEFF"
    ),  # Generic User Property Status + External Supply Voltage Frequency + Read Only + 65533 Hz
    # Generic Admin Property Server
    bytes.fromhex("822C"),  # Generic Admin Properties Get
    bytes.fromhex(
        "47"
        + "9700"
        + "9800"
        + "9900"
        + "9A00"
        + "9C00"
        + "9D00"
        + "9E00"
        + "9F00"
        + "A000"
        + "A400"
        + "A500"
        + "AB00"
        + "AC00"
        + "AD00"
    ),  # Generic Admin Properties Status
    bytes.fromhex("822D" + "7000"),  # Generic Admin Property Get + Total Luminous Energy
    bytes.fromhex(
        "48" + "9400" + "7fff"
    ),  # Generic Admin Property Set + Light Source Temperature + 16383.5 °C
    bytes.fromhex(
        "49" + "A400" + "FFFFFD"
    ),  # Generic Admin Property Set Unacknowledged + Nominal Light Output + 16777213 lm
    bytes.fromhex(
        "4A" + "7300" + "02" + "64"
    ),  # Generic Admin Property Status + Write Only + Power Factor + 100
    # ------------------
    # Generic Manufacturer Property Server
    bytes.fromhex("822A"),  # Generic Manufacturer Properties Get
    bytes.fromhex(
        "43" + "AE00" + "B400" + "B500" + "B600" + "B700"
    ),  # Generic Manufacturer Properties Status
    bytes.fromhex("822B" + "7200"),  # Generic Manufacturer Property Get + Precise Total Device Energy Use
    bytes.fromhex(
        "44" + "8D00" + "FEFFFE"
    ),  # Generic Manufacturer Property Set + Light Source Current + 655.34 A
    bytes.fromhex(
        "45" + "9900" + "5761726d2057686974652020202020202020202020202020"
    ),  # Generic Manufacturer Property Set Unacknowledged + Luminaire Color + "Warm White          "
    bytes.fromhex(
        "46" + "A000" + "03" + "FEFF00"
    ),  # Generic Manufacturer Property Status + Luminaire Time Of Manufacture + Read Write + 12-12-12 2012 12:12
    # ------------------
    # Generic Client Property Server
    bytes.fromhex("4F"),  # Generic Client Properties Get
    bytes.fromhex("50" + "7300"),  # Generic Client Properties Status
    # ------------------
    # Silvair Light Extended Controller
    bytes.fromhex("f63601" + "00" + "71ff"),  # PROPERTY_GET
    bytes.fromhex("f63601" + "01" + "71ff01"),  # PROPERTY_SET
    bytes.fromhex("f63601" + "03" + "72ff90ca04"),  # PROPERTY_STATUS
    # ------------------
    # Silvair EL Server
    bytes.fromhex("EA3601" + "00"),  # EL_INHIBIT_ENTER
    bytes.fromhex("EA3601" + "01"),  # EL_INHIBIT_ENTER_UNACKNOWLEDGED
    bytes.fromhex("EA3601" + "02"),  # EL_INHIBIT_EXIT
    bytes.fromhex("EA3601" + "03"),  # EL_INHIBIT_EXIT_UNACKNOWLEDGED
    bytes.fromhex("EA3601" + "04"),  # EL_STATE_GET
    bytes.fromhex("EA3601" + "05" + "00"),  # EL_STATE_STATUS
    bytes.fromhex("EA3601" + "06" + "80FF"),  # EL_PROPERTY_GET
    bytes.fromhex("EA3601" + "07" + "80FF3412"),  # EL_PROPERTY_SET
    bytes.fromhex("EA3601" + "08" + "80FF3412"),  # EL_PROPERTY_SET_UNACKNOWLEDGED
    bytes.fromhex("EA3601" + "09" + "80FF3412"),  # EL_PROPERTY_STATUS
    bytes.fromhex("EA3601" + "0A"),  # EL_LAMP_OPERATION_TIME_GET
    bytes.fromhex("EA3601" + "0B"),  # EL_LAMP_OPERATION_TIME_CLEAR
    bytes.fromhex("EA3601" + "0C"),  # EL_LAMP_OPERATION_TIME_CLEAR_UNACKNOWLEDGED
    bytes.fromhex("EA3601" + "0D" + "67452301EFCDAB89"),  # EL_LAMP_OPERATION_TIME_STATUS
    bytes.fromhex("EA3601" + "0E"),  # EL_REST_ENTER
    bytes.fromhex("EA3601" + "0F"),  # EL_REST_ENTER_UNACKNOWLEDGED
    bytes.fromhex("EA3601" + "10"),  # EL_REST_EXIT
    bytes.fromhex("EA3601" + "11"),  # EL_REST_EXIT_UNACKNOWLEDGED
    # ------------------
    # Silvair ELT Server
    bytes.fromhex("E93601" + "00"),  # ELT_FUNCTIONAL_TEST_GET
    bytes.fromhex("E93601" + "01"),  # ELT_FUNCTIONAL_TEST_START
    bytes.fromhex("E93601" + "02"),  # ELT_FUNCTIONAL_TEST_STOP
    bytes.fromhex("E93601" + "03" + "05040302010608070506"),  # ELT_FUNCTIONAL_TEST_STATUS
    bytes.fromhex("E93601" + "03" + "0000000000060807050604030201"),  # ELT_FUNCTIONAL_TEST_STATUS
    bytes.fromhex("E93601" + "04"),  # ELT_DURATION_TEST_GET
    bytes.fromhex("E93601" + "05"),  # ELT_DURATION_TEST_START
    bytes.fromhex("E93601" + "06"),  # ELT_DURATION_TEST_STOP
    bytes.fromhex("E93601" + "07" + "050403020106080705063412"),  # ELT_DURATION_TEST_STATUS
    bytes.fromhex("E93601" + "07" + "00000000000608070506341204030201"),  # ELT_DURATION_TEST_STATUS
    bytes.fromhex("E93601" + "08" + "84FF"),  # ELT_PROPERTY_GET
    bytes.fromhex("E93601" + "08" + "85FF"),  # ELT_PROPERTY_GET
    bytes.fromhex("E93601" + "08" + "86FF"),  # ELT_PROPERTY_GET
    bytes.fromhex("E93601" + "08" + "87FF"),  # ELT_PROPERTY_GET
    bytes.fromhex("E93601" + "08" + "88FF"),  # ELT_PROPERTY_GET
    bytes.fromhex("E93601" + "08" + "89FF"),  # ELT_PROPERTY_GET
    bytes.fromhex("E93601" + "08" + "8AFF"),  # ELT_PROPERTY_GET
    bytes.fromhex("E93601" + "08" + "8BFF"),  # ELT_PROPERTY_GET
    bytes.fromhex("E93601" + "09" + "84FF04030201"),  # ELT_PROPERTY_SET
    bytes.fromhex("E93601" + "09" + "85FF04030201"),  # ELT_PROPERTY_SET
    bytes.fromhex("E93601" + "09" + "86FF04030201"),  # ELT_PROPERTY_SET
    bytes.fromhex("E93601" + "09" + "87FF04030201"),  # ELT_PROPERTY_SET
    bytes.fromhex("E93601" + "09" + "88FF04030201"),  # ELT_PROPERTY_SET
    bytes.fromhex("E93601" + "09" + "89FF04030201"),  # ELT_PROPERTY_SET
    bytes.fromhex("E93601" + "09" + "8AFF04030201"),  # ELT_PROPERTY_SET
    bytes.fromhex("E93601" + "09" + "8BFF04030201"),  # ELT_PROPERTY_SET
    bytes.fromhex("E93601" + "0A" + "84FF04030201"),  # ELT_PROPERTY_SET_UNACKNOWLEDGED
    bytes.fromhex("E93601" + "0A" + "85FF04030201"),  # ELT_PROPERTY_SET_UNACKNOWLEDGED
    bytes.fromhex("E93601" + "0A" + "86FF04030201"),  # ELT_PROPERTY_SET_UNACKNOWLEDGED
    bytes.fromhex("E93601" + "0A" + "87FF04030201"),  # ELT_PROPERTY_SET_UNACKNOWLEDGED
    bytes.fromhex("E93601" + "0A" + "88FF04030201"),  # ELT_PROPERTY_SET_UNACKNOWLEDGED
    bytes.fromhex("E93601" + "0A" + "89FF04030201"),  # ELT_PROPERTY_SET_UNACKNOWLEDGED
    bytes.fromhex("E93601" + "0A" + "8AFF04030201"),  # ELT_PROPERTY_SET_UNACKNOWLEDGED
    bytes.fromhex("E93601" + "0A" + "8BFF04030201"),  # ELT_PROPERTY_SET_UNACKNOWLEDGED
    bytes.fromhex("E93601" + "0B" + "84FF04030201"),  # ELT_PROPERTY_STATUS
    bytes.fromhex("E93601" + "0B" + "85FF04030201"),  # ELT_PROPERTY_STATUS
    bytes.fromhex("E93601" + "0B" + "86FF04030201"),  # ELT_PROPERTY_STATUS
    bytes.fromhex("E93601" + "0B" + "87FF04030201"),  # ELT_PROPERTY_STATUS
    bytes.fromhex("E93601" + "0B" + "88FF04030201"),  # ELT_PROPERTY_STATUS
    bytes.fromhex("E93601" + "0B" + "89FF04030201"),  # ELT_PROPERTY_STATUS
    bytes.fromhex("E93601" + "0B" + "8AFF04030201"),  # ELT_PROPERTY_STATUS
    bytes.fromhex("E93601" + "0B" + "8BFF04030201"),  # ELT_PROPERTY_STATUS
]


@pytest.fixture(scope="session")
def capnproto():
    import capnp

    from bluetooth_mesh.messages.capnproto import generate

    with NamedTemporaryFile("w", suffix=".capnp") as f:
        generate(0xD988DA1AAFBE9E47, f)
        f.flush()
        return capnp.load(f.name)


@pytest.mark.skipif(not importlib.util.find_spec("capnp"), reason="requires Python3.7")
@pytest.mark.parametrize("encoded", [pytest.param(i, id=i.hex()) for i in valid])
def test_parse_capnproto(encoded, capnproto):
    logging.info("MESH[%i] %s", len(encoded), encoded.hex())

    decoded = AccessMessage.parse(encoded)
    logging.info("CONSTRUCT %r", decoded)

    params = to_camelcase_dict(decoded)
    logging.info("CAPNP INPUT[%i] %s", len(json.dumps(params)), json.dumps(params))

    message = capnproto.AccessMessage.new_message(**params)
    logging.info("CAPNP %r", message)

    packed = message.to_bytes_packed()
    logging.info("PACKED[%i] %s", len(packed), packed.hex())

    unpacked = capnproto.AccessMessage.from_bytes_packed(packed)
    logging.info("UNPACKED %r", unpacked)

    params = to_snakecase_dict(unpacked.to_dict())
    logging.info("CONSTRUCT INPUT %s", params)

    recoded = AccessMessage.build(params)
    logging.info("RECODED[%i] %s", len(recoded), recoded.hex())

    assert recoded == encoded
