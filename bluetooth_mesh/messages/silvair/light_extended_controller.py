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
from enum import IntEnum

from construct import Construct, Flag, Int8ul, Int16ul, Struct, this

from bluetooth_mesh.messages.properties import PropertyMixin, TimeMiliseconds24
from bluetooth_mesh.messages.util import EnumAdapter, EnumSwitch as Switch, Opcode, SwitchStruct


class LightExtendedControllerOpcode(IntEnum):
    SILVAIR_LEC = 0xF63601


class LightExtendedControllerSubOpcode(IntEnum):
    PROPERTY_GET = 0x00
    PROPERTY_SET = 0x01
    PROPERTY_SET_UNACKNOWLEDGED = 0x02
    PROPERTY_STATUS = 0x03
    BULK_LC_PROPERTY_SET = 0x04
    BULK_LC_PROPERTY_STATUS = 0x05
    BULK_LEC_PROPERTY_SET = 0x06
    BULK_LEC_PROPERTY_STATUS = 0x06
    SYNC_INTEGRAL_GET = 0x08
    SYNC_INTEGRAL_STATUS = 0x09


class LightExtendedControllerProperty(IntEnum):
    AUTO_RESUME_MODE = 0xFF71
    AUTO_RESUME_TIMER = 0xFF72


LightExtendedControllerPropertyDict = {
    LightExtendedControllerProperty.AUTO_RESUME_MODE: Flag,
    LightExtendedControllerProperty.AUTO_RESUME_TIMER: TimeMiliseconds24,
}


class _LightExtendedControllerProperty(PropertyMixin, Construct):
    ENUM = LightExtendedControllerProperty
    DICT = LightExtendedControllerPropertyDict

    subcon = Struct(
        "property_id" / EnumAdapter(Int16ul, LightExtendedControllerProperty),
        Switch(this.id, LightExtendedControllerPropertyDict),
    )

    def _parse(self, stream, context, path):
        msg = LightExtendedControllerPropertyGet._parse(stream, context, path)
        return self._parse_property(msg, stream, context, path)

    def _build(self, obj, stream, context, path):
        LightExtendedControllerPropertyGet._build(obj, stream, context, path)
        return self._build_property(obj, stream, context, path)


# fmt: off
LightExtendedControllerPropertyGet = Struct(
    "property_id" / EnumAdapter(Int16ul, LightExtendedControllerProperty),
)

LightExtendedControllerPropertySet = _LightExtendedControllerProperty()

LightExtendedControllerPropertyStatus = _LightExtendedControllerProperty()

LightExtendedControllerSyncIntegralStatus = Struct(
    "sync_integral" / Int16ul,
)

LightExtendedControllerParams = SwitchStruct(
    "subopcode" / EnumAdapter(Int8ul, LightExtendedControllerSubOpcode),
    "payload" / Switch(
        this.subopcode,
        {
            LightExtendedControllerSubOpcode.PROPERTY_GET: LightExtendedControllerPropertyGet,
            LightExtendedControllerSubOpcode.PROPERTY_SET: LightExtendedControllerPropertySet,
            LightExtendedControllerSubOpcode.PROPERTY_SET_UNACKNOWLEDGED: LightExtendedControllerPropertySet,
            LightExtendedControllerSubOpcode.PROPERTY_STATUS: LightExtendedControllerPropertyStatus,
            LightExtendedControllerSubOpcode.SYNC_INTEGRAL_STATUS: LightExtendedControllerSyncIntegralStatus,
        }
    )
)

LightExtendedControllerMessage = SwitchStruct(
    "opcode" / Opcode(LightExtendedControllerOpcode),
    "params" / Switch(
        this.opcode,
        {
            LightExtendedControllerOpcode.SILVAIR_LEC: LightExtendedControllerParams,
        }
    )
)
# fmt: on
