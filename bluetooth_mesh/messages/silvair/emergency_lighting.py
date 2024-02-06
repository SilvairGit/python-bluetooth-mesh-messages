#
# python-bluetooth-mesh - Bluetooth Mesh for Python
#
# Copyright (C) 2024  SILVAIR sp. z o.o.
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
from enum import IntEnum

from construct import Construct, Int8ul, Int16ul, Int32ul, Struct, this

from bluetooth_mesh.messages.properties import PerceivedLightness, PropertyMixin, TimeSecond16
from bluetooth_mesh.messages.util import EnumAdapter, EnumSwitch as Switch, Opcode, SwitchStruct


class EmergencyLightingOpcode(IntEnum):
    SILVAIR_EL = 0xEA3601


class EmergencyLightingSubOpcode(IntEnum):
    EL_INHIBIT_ENTER = 0x00
    EL_INHIBIT_ENTER_UNACKNOWLEDGED = 0x01
    EL_INHIBIT_EXIT = 0x02
    EL_INHIBIT_EXIT_UNACKNOWLEDGED = 0x03
    EL_STATE_GET = 0x04
    EL_STATE_STATUS = 0x05
    EL_PROPERTY_GET = 0x06
    EL_PROPERTY_SET = 0x07
    EL_PROPERTY_SET_UNACKNOWLEDGED = 0x08
    EL_PROPERTY_STATUS = 0x09
    EL_LAMP_OPERATION_TIME_GET = 0x0A
    EL_LAMP_OPERATION_TIME_CLEAR = 0x0B
    EL_LAMP_OPERATION_TIME_CLEAR_UNACKNOWLEDGED = 0x0C
    EL_LAMP_OPERATION_TIME_STATUS = 0x0D
    EL_REST_ENTER = 0x0E
    EL_REST_ENTER_UNACKNOWLEDGED = 0x0F
    EL_REST_EXIT = 0x10
    EL_REST_EXIT_UNACKNOWLEDGED = 0x11


class ElState(IntEnum):
    TRANSITION_FROM_INHIBIT_TO_NORMAL = 0x00
    TRANSITION_FROM_FUNCTIONAL_TEST_TO_NORMAL = 0x01
    TRANSITION_FROM_DURATION_TEST_TO_NORMAL = 0x02
    NORMAL = 0x03
    TRANSITION_FROM_REST_TO_EMERGENCY = 0x04
    EMERGENCY = 0x05
    EXTENDED_EMERGENCY = 0x06
    TRANSITION_FROM_EMERGENCY_TO_REST = 0x07
    REST = 0x08
    TRANSITION_FROM_NORMAL_TO_INHIBIT = 0x09
    INHIBIT = 0x0A
    TRANSITION_FROM_NORMAL_TO_DURATION_TEST = 0x0B
    DURATION_TEST_IN_PROGRESS = 0x0C
    TRANSITION_FROM_NORMAL_TO_FUNCTIONAL_TEST = 0x0D
    FUNCTIONAL_TEST_IN_PROGRESS = 0x0E
    BATTERY_DISCHARGED = 0x0F
    UNKNOWN = 0x10


class EmergencyLightingProperty(IntEnum):
    EL_LIGHTNESS = 0xFF80
    EL_LIGHTNESS_RANGE_MIN = 0xFF81
    EL_LIGHTNESS_RANGE_MAX = 0xFF82
    EL_PROLONG_TIME = 0xFF83


EmergencyLightingPropertyDict = {
    EmergencyLightingProperty.EL_LIGHTNESS: PerceivedLightness,
    EmergencyLightingProperty.EL_LIGHTNESS_RANGE_MIN: PerceivedLightness,
    EmergencyLightingProperty.EL_LIGHTNESS_RANGE_MAX: PerceivedLightness,
    EmergencyLightingProperty.EL_PROLONG_TIME: TimeSecond16,
}


class _EmergencyLightingProperty(PropertyMixin, Construct):
    ENUM = EmergencyLightingProperty
    DICT = EmergencyLightingPropertyDict

    subcon = Struct(
        "property_id" / EnumAdapter(Int16ul, EmergencyLightingProperty),
        Switch(this.id, EmergencyLightingPropertyDict),
    )

    def _parse(self, stream, context, path):
        msg = EmergencyLightingPropertyGet._parse(stream, context, path)
        return self._parse_property(msg, stream, context, path)

    def _build(self, obj, stream, context, path):
        EmergencyLightingPropertyGet._build(obj, stream, context, path)
        return self._build_property(obj, stream, context, path)


# fmt: off
EmergencyLightingInhibitEnter = Struct()

EmergencyLightingInhibitExit = Struct()

EmergencyLightingStateGet = Struct()

EmergencyLightingStateStatus = Struct(
    "el_state" / EnumAdapter(Int8ul, ElState),
)

EmergencyLightingPropertyGet = Struct(
    "property_id" / EnumAdapter(Int16ul, EmergencyLightingProperty),
)

EmergencyLightingPropertySet = _EmergencyLightingProperty()

EmergencyLightingPropertyStatus = _EmergencyLightingProperty()

EmergencyLightingLampOperationTimeGet = Struct()

EmergencyLightingLampOperationTimeClear = Struct()

EmergencyLightingLampOperationTimeStatus = Struct(
    "el_lamp_total_operation_time" / Int32ul,
    "el_lamp_emergency_time" / Int32ul,
)

EmergencyLightingRestEnter = Struct()

EmergencyLightingRestExit = Struct()

EmergencyLightingParams = SwitchStruct(
    "subopcode" / EnumAdapter(Int8ul, EmergencyLightingSubOpcode),
    "payload" / Switch(
        this.subopcode,
        {
            EmergencyLightingSubOpcode.EL_INHIBIT_ENTER: EmergencyLightingInhibitEnter,
            EmergencyLightingSubOpcode.EL_INHIBIT_ENTER_UNACKNOWLEDGED: EmergencyLightingInhibitEnter,
            EmergencyLightingSubOpcode.EL_INHIBIT_EXIT: EmergencyLightingInhibitExit,
            EmergencyLightingSubOpcode.EL_INHIBIT_EXIT_UNACKNOWLEDGED: EmergencyLightingInhibitExit,
            EmergencyLightingSubOpcode.EL_STATE_GET: EmergencyLightingStateGet,
            EmergencyLightingSubOpcode.EL_STATE_STATUS: EmergencyLightingStateStatus,
            EmergencyLightingSubOpcode.EL_PROPERTY_GET: EmergencyLightingPropertyGet,
            EmergencyLightingSubOpcode.EL_PROPERTY_SET: EmergencyLightingPropertySet,
            EmergencyLightingSubOpcode.EL_PROPERTY_SET_UNACKNOWLEDGED: EmergencyLightingPropertySet,
            EmergencyLightingSubOpcode.EL_PROPERTY_STATUS: EmergencyLightingPropertyStatus,
            EmergencyLightingSubOpcode.EL_LAMP_OPERATION_TIME_GET: EmergencyLightingLampOperationTimeGet,
            EmergencyLightingSubOpcode.EL_LAMP_OPERATION_TIME_CLEAR: EmergencyLightingLampOperationTimeClear,
            EmergencyLightingSubOpcode.EL_LAMP_OPERATION_TIME_CLEAR_UNACKNOWLEDGED: EmergencyLightingLampOperationTimeClear,
            EmergencyLightingSubOpcode.EL_LAMP_OPERATION_TIME_STATUS: EmergencyLightingLampOperationTimeStatus,
            EmergencyLightingSubOpcode.EL_REST_ENTER: EmergencyLightingRestEnter,
            EmergencyLightingSubOpcode.EL_REST_ENTER_UNACKNOWLEDGED: EmergencyLightingRestEnter,
            EmergencyLightingSubOpcode.EL_REST_EXIT: EmergencyLightingRestExit,
            EmergencyLightingSubOpcode.EL_REST_EXIT_UNACKNOWLEDGED: EmergencyLightingRestExit,
        }
    )
)

EmergencyLightingMessage = SwitchStruct(
    "opcode" / Opcode(EmergencyLightingOpcode),
    "params" / Switch(
        this.opcode,
        {
            EmergencyLightingOpcode.SILVAIR_EL: EmergencyLightingParams
        }
    )
)
# fmt: on
