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

from construct import Construct, Embedded, GreedyRange, Int8ul, Int16ul, Struct, this

from bluetooth_mesh.messages.properties import PropertyDict, PropertyID, PropertyMixin
from bluetooth_mesh.messages.sensor import SensorPropertyId, SensorSettingAccess
from bluetooth_mesh.messages.util import EnumAdapter, EnumSwitch as Switch, Opcode, SwitchStruct


class GenericPropertyOpcode(IntEnum):
    GENERIC_USER_PROPERTIES_GET = 0x822E
    GENERIC_USER_PROPERTIES_STATUS = 0x4B
    GENERIC_USER_PROPERTY_GET = 0x822F
    GENERIC_USER_PROPERTY_SET = 0x4C
    GENERIC_USER_PROPERTY_SET_UNACKNOWLEDGED = 0x4D
    GENERIC_USER_PROPERTY_STATUS = 0x4E
    GENERIC_ADMIN_PROPERTIES_GET = 0x822C
    GENERIC_ADMIN_PROPERTIES_STATUS = 0x47
    GENERIC_ADMIN_PROPERTY_GET = 0x822D
    GENERIC_ADMIN_PROPERTY_SET = 0x48
    GENERIC_ADMIN_PROPERTY_SET_UNACKNOWLEDGED = 0x49
    GENERIC_ADMIN_PROPERTY_STATUS = 0x4A
    GENERIC_MANUFACTURER_PROPERTIES_GET = 0x822A
    GENERIC_MANUFACTURER_PROPERTIES_STATUS = 0x43
    GENERIC_MANUFACTURER_PROPERTY_GET = 0x822B
    GENERIC_MANUFACTURER_PROPERTY_SET = 0x44
    GENERIC_MANUFACTURER_PROPERTY_SET_UNACKNOWLEDGED = 0x45
    GENERIC_MANUFACTURER_PROPERTY_STATUS = 0x46
    GENERIC_CLIENT_PROPERTIES_GET = 0x4F
    GENERIC_CLIENT_PROPERTIES_STATUS = 0x50


GenericPropertiesGet = Struct()

GenericPropertiesStatus = Struct(
    "property_ids" / GreedyRange(SensorPropertyId),
)

GenericPropertyGet = Struct(
    "property_id" / SensorPropertyId,
)


class _GenericPropertySet(PropertyMixin, Construct):
    ENUM = PropertyID
    DICT = PropertyDict

    subcon = Struct(
        "property_id" / EnumAdapter(Int16ul, PropertyID),
        Switch(this.id, PropertyDict),
    )

    def _parse(self, stream, context, path):
        msg = GenericPropertyGet._parse(stream, context, path)
        return self._parse_property(msg, stream, context, path)

    def _build(self, obj, stream, context, path):
        GenericPropertyGet._build(obj, stream, context, path)
        return self._build_property(obj, stream, context, path)


class _GenericPropertyStatus(PropertyMixin, Construct):
    ENUM = PropertyID
    DICT = PropertyDict

    subcon = Struct(
        "property_id" / EnumAdapter(Int16ul, PropertyID),
        "access" / EnumAdapter(Int8ul, SensorSettingAccess),
        Switch(this.id, PropertyDict),
    )

    def _parse(self, stream, context, path):
        msg = Struct(Embedded(GenericPropertyGet), "access" / Int8ul)._parse(stream, context, path)
        return self._parse_property(msg, stream, context, path)

    def _build(self, obj, stream, context, path):
        Struct(Embedded(GenericPropertyGet), "access" / Int8ul)._build(obj, stream, context, path)
        return self._build_property(obj, stream, context, path)


GenericPropertySet = _GenericPropertySet()

GenericPropertyStatus = _GenericPropertyStatus()

GenericPropertyMessage = SwitchStruct(
    "opcode" / Opcode(GenericPropertyOpcode),
    "params"
    / Switch(
        this.opcode,
        {
            GenericPropertyOpcode.GENERIC_USER_PROPERTIES_GET: GenericPropertiesGet,
            GenericPropertyOpcode.GENERIC_USER_PROPERTIES_STATUS: GenericPropertiesStatus,
            GenericPropertyOpcode.GENERIC_USER_PROPERTY_GET: GenericPropertyGet,
            GenericPropertyOpcode.GENERIC_USER_PROPERTY_SET: GenericPropertySet,
            GenericPropertyOpcode.GENERIC_USER_PROPERTY_SET_UNACKNOWLEDGED: GenericPropertySet,
            GenericPropertyOpcode.GENERIC_USER_PROPERTY_STATUS: GenericPropertyStatus,
            GenericPropertyOpcode.GENERIC_ADMIN_PROPERTIES_GET: GenericPropertiesGet,
            GenericPropertyOpcode.GENERIC_ADMIN_PROPERTIES_STATUS: GenericPropertiesStatus,
            GenericPropertyOpcode.GENERIC_ADMIN_PROPERTY_GET: GenericPropertyGet,
            GenericPropertyOpcode.GENERIC_ADMIN_PROPERTY_SET: GenericPropertySet,
            GenericPropertyOpcode.GENERIC_ADMIN_PROPERTY_SET_UNACKNOWLEDGED: GenericPropertySet,
            GenericPropertyOpcode.GENERIC_ADMIN_PROPERTY_STATUS: GenericPropertyStatus,
            GenericPropertyOpcode.GENERIC_MANUFACTURER_PROPERTIES_GET: GenericPropertiesGet,
            GenericPropertyOpcode.GENERIC_MANUFACTURER_PROPERTIES_STATUS: GenericPropertiesStatus,
            GenericPropertyOpcode.GENERIC_MANUFACTURER_PROPERTY_GET: GenericPropertyGet,
            GenericPropertyOpcode.GENERIC_MANUFACTURER_PROPERTY_SET: GenericPropertySet,
            GenericPropertyOpcode.GENERIC_MANUFACTURER_PROPERTY_SET_UNACKNOWLEDGED: GenericPropertySet,
            GenericPropertyOpcode.GENERIC_MANUFACTURER_PROPERTY_STATUS: GenericPropertyStatus,
            GenericPropertyOpcode.GENERIC_CLIENT_PROPERTIES_GET: GenericPropertiesGet,
            GenericPropertyOpcode.GENERIC_CLIENT_PROPERTIES_STATUS: GenericPropertiesStatus,
        },
    ),
)
