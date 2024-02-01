#
# python-bluetooth-mesh - Bluetooth Mesh for Python
#
# Copyright (C) 2023  SILVAIR sp. z o.o.
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
from datetime import datetime, timedelta, timezone
from enum import IntEnum

from construct import (
    Adapter,
    BitsInteger,
    BitStruct,
    BytesInteger,
    Const,
    Construct,
    Container,
    Embedded,
    Flag,
    Int8ul,
    Int16sl,
    Int16ul,
    Int32ul,
    Padding,
    Struct,
    this,
)

from bluetooth_mesh.messages.properties import PropertyDict, PropertyMixin, TimeSecond32
from bluetooth_mesh.messages.time import (
    MESH_UNIX_EPOCH_DIFF,
    DateTime,
    TAIUTCDeltaAdapter,
    mesh_tai_utc_delta_to_timedelta,
    mesh_time_zone_offset_to_timedelta,
    timedelta_to_mesh_tai_utc_delta,
    timedelta_to_mesh_time_zone_offset,
)
from bluetooth_mesh.messages.util import (
    AliasedContainer,
    EmbeddedBitStruct,
    EnumAdapter,
    EnumSwitch as Switch,
    NamedSelect,
    Opcode,
    SwitchStruct,
)


class EmergencyLightingTestOpcode(IntEnum):
    SILVAIR_ELT = 0xE93601


class EmergencyLightingTestSubOpcode(IntEnum):
    ELT_FUNCTIONAL_TEST_GET = 0x00
    ELT_FUNCTIONAL_TEST_START = 0x01
    ELT_FUNCTIONAL_TEST_STOP = 0x02
    ELT_FUNCTIONAL_TEST_STATUS = 0x03
    ELT_DURATION_TEST_GET = 0x04
    ELT_DURATION_TEST_START = 0x05
    ELT_DURATION_TEST_STOP = 0x06
    ELT_DURATION_TEST_STATUS = 0x07
    ELT_PROPERTY_GET = 0x08
    ELT_PROPERTY_SET = 0x09
    ELT_PROPERTY_SET_UNACKNOWLEDGED = 0x0A
    ELT_PROPERTY_STATUS = 0x0B


class TestExecutionStatus(IntEnum):
    FINISHED = 0
    TRIGGERED = 1
    IN_PROGRESS = 2
    POSTPONED = 3
    STOPPED = 4
    DROPPED = 5
    TIMEOUT = 6
    UNKNOWN = 7


FunctionalExecutionResult = BitStruct(
    Padding(5),
    "circuit_fault" / Flag,
    "battery_fault" / Flag,
    "lamp_fault" / Flag,
)

DurationExecutionResult = BitStruct(
    Padding(4),
    "battery_duration_fault" / Flag,
    "circuit_fault" / Flag,
    "battery_fault" / Flag,
    "lamp_fault" / Flag,
)


class TimestampAdapter(Adapter):
    _subcon = Struct(
        "date" / DateTime,
        "tai_utc_delta" / TAIUTCDeltaAdapter(Int16sl),
    )

    def _decode(self, obj, context, path):
        time_zone_offset = mesh_time_zone_offset_to_timedelta(obj["time_zone_offset"])
        full_recv_time = obj["tai_seconds"] + MESH_UNIX_EPOCH_DIFF + int(time_zone_offset.total_seconds())
        recv_date = datetime.fromtimestamp(full_recv_time, timezone(time_zone_offset))

        return Container(
            date=recv_date,
            tai_utc_delta=mesh_tai_utc_delta_to_timedelta(obj["tai_utc_delta"]),
        )

    def _encode(self, obj, context, path):
        passed_time: datetime = obj["date"]

        if isinstance(passed_time, dict):  # capnproto message
            time_zone = timedelta(minutes=passed_time["time_zone_offset"])
            passed_time = datetime(
                year=passed_time["year"],
                month=passed_time["month"],
                day=passed_time["day"],
                hour=passed_time["hour"],
                minute=passed_time["minute"],
                second=passed_time["second"],
                microsecond=passed_time["microsecond"],
                tzinfo=timezone(time_zone),
            )

        if isinstance(obj["tai_utc_delta"], int):
            obj["tai_utc_delta"] = timedelta(seconds=obj["tai_utc_delta"])

        total_time = passed_time.timestamp() - MESH_UNIX_EPOCH_DIFF - passed_time.utcoffset().total_seconds()

        return Container(
            tai_seconds=int(total_time),
            tai_utc_delta=timedelta_to_mesh_tai_utc_delta(obj["tai_utc_delta"]),
            time_zone_offset=timedelta_to_mesh_time_zone_offset(passed_time.utcoffset()),
        )


class EmergencyLightingTestProperty(IntEnum):
    ELT_DURATION_TEST_EXECUTION_TIMEOUT = 0xFF84
    ELT_FUNCTIONAL_TEST_EXECUTION_TIMEOUT = 0xFF85
    ELT_DURATION_TEST_RETRY_PERIOD = 0xFF86
    ELT_FUNCTIONAL_TEST_RETRY_PERIOD = 0xFF87
    ELT_DURATION_TEST_BACKUP_AUTOMATIC_DELAY = 0xFF88
    ELT_FUNCTIONAL_TEST_BACKUP_AUTOMATIC_DELAY = 0xFF89
    ELT_DURATION_TEST_BACKUP_AUTOMATIC_INTERVAL = 0xFF8A
    ELT_FUNCTIONAL_TEST_BACKUP_AUTOMATIC_INTERVAL = 0xFF8B


EmergencyLightingTestPropertyDict = {
    EmergencyLightingTestProperty.ELT_DURATION_TEST_EXECUTION_TIMEOUT: TimeSecond32,
    EmergencyLightingTestProperty.ELT_FUNCTIONAL_TEST_EXECUTION_TIMEOUT: TimeSecond32,
    EmergencyLightingTestProperty.ELT_DURATION_TEST_RETRY_PERIOD: TimeSecond32,
    EmergencyLightingTestProperty.ELT_FUNCTIONAL_TEST_RETRY_PERIOD: TimeSecond32,
    EmergencyLightingTestProperty.ELT_DURATION_TEST_BACKUP_AUTOMATIC_DELAY: TimeSecond32,
    EmergencyLightingTestProperty.ELT_FUNCTIONAL_TEST_BACKUP_AUTOMATIC_DELAY: TimeSecond32,
    EmergencyLightingTestProperty.ELT_DURATION_TEST_BACKUP_AUTOMATIC_INTERVAL: TimeSecond32,
    EmergencyLightingTestProperty.ELT_FUNCTIONAL_TEST_BACKUP_AUTOMATIC_INTERVAL: TimeSecond32,
}


class _EmergencyLightingTestProperty(PropertyMixin, Construct):
    ENUM = EmergencyLightingTestProperty
    DICT = EmergencyLightingTestPropertyDict

    subcon = Struct(
        "property_id" / EnumAdapter(Int16ul, EmergencyLightingTestProperty),
        Switch(this.id, EmergencyLightingTestPropertyDict),
    )

    def _parse(self, stream, context, path):
        msg = EmergencyLightingTestPropertyGet._parse(stream, context, path)
        return self._parse_property(msg, stream, context, path)

    def _build(self, obj, stream, context, path):
        EmergencyLightingTestPropertyGet._build(obj, stream, context, path)
        return self._build_property(obj, stream, context, path)


# fmt: off
Timestamp = Struct(
    "tai_seconds" / BytesInteger(5, swapped=True),
    "time_zone_offset" / Int8ul,
    *EmbeddedBitStruct("_",
                       Const(0, BitsInteger(1)),
                       "tai_utc_delta" / BitsInteger(15),
                       )
)

EmergencyLightingTestFunctionalTestGet = Struct()

EmergencyLightingTestFunctionalTestStart = Struct()

EmergencyLightingTestFunctionalTestStop = Struct()

EmergencyLightingTestFunctionalTestStatusMinimal = Struct(
    "tai_timestamp" / TimestampAdapter(Timestamp),
    "execution_status" / EnumAdapter(Int8ul, TestExecutionStatus),
    "execution_result" / FunctionalExecutionResult,
)

EmergencyLightingTestFunctionalTestStatusOptional = Struct(
    Embedded(EmergencyLightingTestFunctionalTestStatusMinimal),
    "relative_timestamp" / Int32ul,
)

EmergencyLightingTestFunctionalTestStatus = NamedSelect(
    optional=EmergencyLightingTestFunctionalTestStatusOptional,
    minimal=EmergencyLightingTestFunctionalTestStatusMinimal,
)

EmergencyLightingTestDurationTestGet = Struct()

EmergencyLightingTestDurationTestStart = Struct()

EmergencyLightingTestDurationTestStop = Struct()

EmergencyLightingTestDurationTestStatusMinimal = Struct(
    "tai_timestamp" / TimestampAdapter(Timestamp),
    "execution_status" / EnumAdapter(Int8ul, TestExecutionStatus),
    "execution_result" / DurationExecutionResult,
    "duration_result" / Int16ul,
)

EmergencyLightingTestDurationTestStatusOptional = Struct(
    Embedded(EmergencyLightingTestDurationTestStatusMinimal),
    "relative_timestamp" / Int32ul,
)

EmergencyLightingTestDurationTestStatus = NamedSelect(
    optional=EmergencyLightingTestDurationTestStatusOptional,
    minimal=EmergencyLightingTestDurationTestStatusMinimal,
)


EmergencyLightingTestPropertyGet = Struct(
    "property_id" / EnumAdapter(Int16ul, EmergencyLightingTestProperty),
)

EmergencyLightingTestPropertySet = _EmergencyLightingTestProperty()

EmergencyLightingTestPropertyStatus = _EmergencyLightingTestProperty()


EmergencyLightingTestParams = SwitchStruct(
    "subopcode" / EnumAdapter(Int8ul, EmergencyLightingTestSubOpcode),
    "payload" / Switch(
        this.subopcode,
        {
            EmergencyLightingTestSubOpcode.ELT_FUNCTIONAL_TEST_GET: EmergencyLightingTestFunctionalTestGet,
            EmergencyLightingTestSubOpcode.ELT_FUNCTIONAL_TEST_START: EmergencyLightingTestFunctionalTestStart,
            EmergencyLightingTestSubOpcode.ELT_FUNCTIONAL_TEST_STOP: EmergencyLightingTestFunctionalTestStop,
            EmergencyLightingTestSubOpcode.ELT_FUNCTIONAL_TEST_STATUS: EmergencyLightingTestFunctionalTestStatus,
            EmergencyLightingTestSubOpcode.ELT_DURATION_TEST_GET: EmergencyLightingTestDurationTestGet,
            EmergencyLightingTestSubOpcode.ELT_DURATION_TEST_START: EmergencyLightingTestDurationTestStart,
            EmergencyLightingTestSubOpcode.ELT_DURATION_TEST_STOP: EmergencyLightingTestDurationTestStop,
            EmergencyLightingTestSubOpcode.ELT_DURATION_TEST_STATUS: EmergencyLightingTestDurationTestStatus,
            EmergencyLightingTestSubOpcode.ELT_PROPERTY_GET: EmergencyLightingTestPropertyGet,
            EmergencyLightingTestSubOpcode.ELT_PROPERTY_SET: EmergencyLightingTestPropertySet,
            EmergencyLightingTestSubOpcode.ELT_PROPERTY_SET_UNACKNOWLEDGED: EmergencyLightingTestPropertySet,
            EmergencyLightingTestSubOpcode.ELT_PROPERTY_STATUS: EmergencyLightingTestPropertyStatus,
        }
    )
)

EmergencyLightingTestMessage = SwitchStruct(
    "opcode" / Opcode(EmergencyLightingTestOpcode),
    "params" / Switch(
        this.opcode,
        {
            EmergencyLightingTestOpcode.SILVAIR_ELT: EmergencyLightingTestParams
        }
    )
)
# fmt: on
