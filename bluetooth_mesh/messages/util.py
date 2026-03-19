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

import enum
import math
import re
import sys
from collections.abc import Mapping
from datetime import date, datetime, timedelta
from ipaddress import IPv4Address

from construct import (
    Adapter,
    Bit,
    BitStruct,
    Bitwise,
    Computed,
    Construct,
    Container,
    Enum,
    ExprValidator,
    Float64b,
    FuncPath,
    IfThenElse,
    Int32ub,
    Pass,
    Rebuild,
    Restreamed,
    Select,
    SizeofError,
    Struct,
    Switch,
    ValidationError,
    stream_read,
    stream_write,
    this,
)


def identity(x):
    return x


def reverse(sequence):
    return sequence[::-1]


def Reversed(subcon):
    return Restreamed(subcon, reverse, subcon.sizeof(), reverse, subcon.sizeof(), identity)


class BitListAdapter(Adapter):
    def __init__(self, subcon, reverse_bits):
        super().__init__(subcon)
        self.reversed = reverse_bits

    def _decode(self, obj, content, path):
        bits = set()

        for bit, feature in enumerate(reversed(obj) if self.reversed else obj):
            if not feature:
                continue

            bits.add(bit)

        return bits

    def _encode(self, obj, content, path):
        bits = []

        for bit in range(self.sizeof() * 8):
            bits.append(bit in obj)

        return list(reversed(bits)) if self.reversed else bits


def BitList(size, *, reversed=False):  # pylint: disable=redefined-builtin
    return BitListAdapter(Bitwise(Bit[size * 8]), reversed)


class SetAdapter(Adapter):
    def _decode(self, obj, context, path):
        return set(obj)

    def _encode(self, obj, context, path):
        return obj


def EnumAdapter(subcon, enum_cls):
    class _Enum(Enum):
        ENUM = enum_cls

    class _EnumAdapter(Adapter):
        type = enum_cls
        _enum = enum_cls

        def _decode(self, obj, context, path):
            if obj not in enum_cls._value2member_map_:
                raise ValidationError(f"object failed validation: '{obj}' not in {enum_cls}")
            return enum_cls(obj)

        def _encode(self, obj, context, path):
            if obj == enum_cls:
                return obj.value

            try:
                return enum_cls[obj] if isinstance(obj, str) else enum_cls(obj)
            except ValueError as ex:
                raise ValidationError(f"object failed validation: '{obj}' not in {enum_cls}") from ex

    _EnumAdapter.__construct_doc__ = _Enum(subcon, enum_cls)

    return _EnumAdapter(subcon)


def LogAdapter(subcon, *, max_value=None, infinity=False):
    class _LogAdapter(Adapter):
        MAX_TYPE_VALUE = int(math.pow(2, subcon.length * 8) - 1)
        _subcon = subcon

        def _decode(self, obj, context, path):
            if obj == 0:
                return 0

            if obj == self.MAX_TYPE_VALUE:
                if infinity:
                    return float("inf")

            if max_value is not None and obj > max_value:
                raise ValidationError(f"max value exceeded, expecting at most {max_value}: {obj}")

            return int(math.pow(2, obj - 1))

        def _encode(self, obj, context, path):
            if obj == 0:
                return 0

            if obj == float("inf"):
                if infinity:
                    return self.MAX_TYPE_VALUE

                raise ValidationError(f"infinity is not allowed: {obj}")

            value = math.log(obj, 2) + 1

            if max_value is not None and value > max_value:
                raise ValidationError(f"max value exceeded, expecting at most {max_value}: {obj}")

            return int(value)

    return _LogAdapter(subcon)


def RangeValidator(subcon, *, min_value=None, max_value=None):
    def validate_range(obj, ctx):
        if min_value is not None and obj < min_value:
            return False

        if max_value is not None and obj > max_value:
            return False

        return True

    return ExprValidator(subcon, validate_range)


class FieldAdapter(Adapter):
    def __init__(self, subcon, field):
        self._subcon = field
        super().__init__(subcon)

    def _decode(self, obj, content, path):
        return obj

    def _encode(self, obj, content, path):
        return obj


def EmbeddedBitStruct(name, *fields, reversed=False):  # pylint: disable=redefined-builtin
    """
    Emulates BitStruct embedding:
        - for parsing, adds Computed accessor fields to the parent construct,
        - for building, Rebuild the bit struct using keys passed to the parent

    NOTE: This is a hack. Do not use unless you absolutely have to.
    """
    bit_struct = BitStruct(*fields)

    if reversed:
        bit_struct = Reversed(bit_struct)

    bit_struct.__construct_doc__ = Struct(*fields)

    return (
        name / Rebuild(bit_struct, dict),
        *(
            field.name / FieldAdapter(Computed(this[name][field.name]), field)
            for field in fields
            if field.name is not None
        ),
    )


class Opcode(Construct):
    __construct_doc__ = Int32ub
    subcon = Int32ub

    def __init__(self, opcode_type=int):
        super().__init__()
        self.type = opcode_type

    def _parse(self, stream, context, path):  # pylint: disable=inconsistent-return-statements
        try:
            opcode = stream_read(stream, 1, path)[0]

            if opcode == 0x7F:
                raise ValidationError

            opcode_len = opcode >> 7

            # 1 byte opcode
            if not opcode_len:
                return self.type(opcode)

            opcode_len = opcode >> 6
            opcode = opcode << 8 | stream_read(stream, 1, path)[0]

            # 2 byte opcode
            if opcode_len == 2:
                return self.type(opcode)

            if opcode_len == 3:
                opcode = opcode << 8 | stream_read(stream, 1, path)[0]
                return self.type(opcode)

            raise ValidationError
        except ValueError as ex:
            raise ValidationError from ex

    def _build(self, obj, stream, context, path):
        if obj > 0xFFFF:
            encoded = obj.to_bytes(3, byteorder="big")
            stream_write(stream, encoded, len(encoded), path)
        elif obj > 0xFF:
            encoded = obj.to_bytes(2, byteorder="big")
            stream_write(stream, encoded, len(encoded), path)
        else:
            encoded = obj.to_bytes(1, byteorder="big")
            stream_write(stream, encoded, len(encoded), path)

        return self.type(obj)

    def _sizeof(self, context, path):
        raise SizeofError


class DefaultCountValidator(Adapter):
    _subcon = Float64b

    def __init__(self, subcon, rounding=None, resolution=1.0, unknown_value=True):
        super().__init__(subcon)
        self.rounding = rounding
        self.resolution = resolution
        self.unknown_value = unknown_value

    def _decode(self, obj, content, path):
        if self.unknown_value and obj == (256**self.subcon.length) - 1:
            return float(sys.float_info.max)
        return round(obj * self.resolution, self.rounding) if self.rounding else obj * self.resolution

    def _encode(self, obj, content, path):
        if self.unknown_value and obj == float(sys.float_info.max):
            return (256**self.subcon.length) - 1
        return round(obj / self.resolution)


class MacAddressAdapter(Adapter):
    def _decode(self, obj, context, path):
        return ":".join(f"{item:02x}" for item in obj)

    def _encode(self, obj, context, path):
        return bytes(int(i, 16) for i in obj.split(":"))


class IpAddressAdapter(Adapter):
    def _decode(self, obj, context, path):
        return IPv4Address(obj)

    def _encode(self, obj, context, path):
        return bytes(int(i) for i in obj.split("."))


class AliasedContainer(Container):
    ALIAS = None
    ORIGINAL = None

    def __getattr__(self, name):
        if name == self.ORIGINAL:
            name = self.ALIAS

        return super().__getattr__(name)

    def __getitem__(self, name):
        if name == self.ORIGINAL:
            name = self.ALIAS

        return super().__getitem__(name)


def _normalize_container_items(value):
    if not isinstance(value, Mapping):
        return None
    return {k: v for k, v in value.items() if not str(k).startswith("_") and v is not None}


def _container_eq_compat(self, other):
    self_items = _normalize_container_items(self)
    other_items = _normalize_container_items(other)
    if self_items is None or other_items is None:
        return NotImplemented
    return all(k in other_items and other_items[k] == v for k, v in self_items.items())


Container.__eq__ = _container_eq_compat


class EnumSwitch(Switch):
    def _emitparse(self, code):
        fname = f"factory_{code.allocateId()}"
        code.append(
            f"{fname} = {{"
            + ", ".join(
                f"{int(key)!r} : lambda io,this: {sc._compileparse(code)}" for key, sc in self.cases.items()
            )
            + "}"
        )

        defaultfname = f"compiled_{code.allocateId()}"
        code.append(f"{defaultfname} = lambda io,this: {self.default._compileparse(code)}")
        return f"{fname}.get({self.keyfunc}, {defaultfname})(io, this)"


class EnumSwitchStruct(Adapter):
    def __init__(self, subcon):
        assert isinstance(subcon, EnumSwitch), "subcon must be an EnumSwitch"
        assert subcon.default is Pass, "subcon must have a default Pass"

        super().__init__(subcon)

    def _decode(self, obj, context, path):
        keyfunc = self.subcon.keyfunc
        if callable(keyfunc):
            keyfunc = keyfunc(context)

        assert isinstance(keyfunc, enum.Enum), "keyfunc must be an enum"

        return {keyfunc.name.lower(): obj}

    def _encode(self, obj, context, path):
        keyfunc = self.subcon.keyfunc
        if callable(keyfunc):
            keyfunc = keyfunc(context)

        mapping = {_enum.value: _enum.name.lower() for _enum in self.subcon.cases.keys()}
        key = mapping[keyfunc]

        return obj[key]


enum_switch_struct_len_ = FuncPath(lambda arg: len(next(iter(arg.values()))))


class SwitchStruct(Adapter):
    def __init__(self, key, switch):
        super().__init__(Struct(key, switch))
        self.key = key
        self.switch = switch
        self._subcon = Struct(key, switch.subcon)

    def _decode(self, obj, context, path):
        key = self.switch.keyfunc(obj)

        try:
            value = obj[self.switch.name]
        except KeyError:
            value = obj[key.name.lower()]

        class _Container(AliasedContainer):
            ORIGINAL = self.switch.name
            ALIAS = key.name.lower()

        return _Container({self.key.name: key, key.name.lower(): value})

    def _encode(self, obj, context, path):
        keytype = self.key.subcon.type
        key = keytype(self.switch.keyfunc(obj))

        try:
            value = obj[key.name.lower()]
        except KeyError:
            value = obj[self.switch.name]

        return Container({self.key.name: key, self.switch.name: value})

    def _emitparse(self, code):
        keytype = self.key.subcon.type

        fname = f"parse_struct_{code.allocateId()}"
        block = f"""
            def {fname}(io, this):
                from {keytype.__module__} import {keytype.__name__}

                key = {self.key._compileparse(code)}
                key_name = {keytype.__name__}(key).name.lower()

                result = Container()
                this = Container(_ = this, _params = this['_params'], _root = None, _parsing = True, _building = False, _sizing = False, _subcons = None, _io = io, _index = this.get('_index', None))
                this['_root'] = this['_'].get('_root', this)
                try:
                    result[{self.key.name!r}] = this[{self.key.name!r}] = key
                    result[key_name] = this[key_name] = {self.switch._compileparse(code)}
                except StopFieldError:
                    pass
                return result
        """
        code.append(block)
        return f"{fname}(io, this)"


class NameAdapter(Adapter):
    def _decode(self, obj, context, path):
        obj._name = self.subcon.name
        return obj

    def _encode(self, obj, context, path):
        return obj.get(self.subcon.name, obj)


class NamedSelect(Adapter):
    def __init__(self, **subconskw):
        subcons = [NameAdapter(k / v) for k, v in subconskw.items()]
        super().__init__(Select(*subcons))
        self.__construct_doc__ = self._subcon = Select(**subconskw)

    def _decode(self, obj, context, path):
        return obj

    def _encode(self, obj, context, path):
        return obj


class IfThenElseDefault(IfThenElse):
    def __init__(self, condfunc, thensubcon, default):
        super().__init__(condfunc, thensubcon, Pass)
        self.condfunc = condfunc
        self.thensubcon = thensubcon
        self.default = default

    def _parse(self, stream, context, path):
        condfunc = self.condfunc
        if callable(condfunc):
            condfunc = condfunc(context)
        return self.thensubcon._parsereport(stream, context, path) if condfunc else self.default


class SwitchWithNamedDefault(Switch):
    def __init__(self, keyfunc, cases, default=None, name_for_default=None):
        self.name_for_default = name_for_default
        super().__init__(keyfunc, cases, default)


def camelcase(field_name):
    if field_name is None:
        return None

    head, *tail = str(field_name).lower().replace(" ", "_").split("_")
    return "".join([head, *(i.title() for i in tail)])


def snakecase(camel_input):
    words = re.findall(r"[A-Z]?[a-z\d]+|[A-Z]{1,}(?=[A-Z][a-z]|\d|\W|$)|\d+", camel_input)
    return "_".join(map(str.lower, words))


def to_case_dict(value, case):
    if isinstance(value, dict):
        new_dict = {case(k): to_case_dict(v, case) for k, v in value.items() if not k.startswith("_")}

        name = getattr(value, "_name", None)
        return {name: new_dict} if name else new_dict

    if isinstance(value, (set, list)):
        return [to_case_dict(i, case) for i in value]

    if isinstance(value, enum.Enum):
        return value.value

    if isinstance(value, bytes):
        return value.hex()

    if isinstance(value, datetime):
        return {
            "year": value.year,
            "month": value.month,
            "day": value.day,
            "hour": value.hour,
            "minute": value.minute,
            "second": value.second,
            "microsecond": value.microsecond,
            "timeZoneOffset": (value.utcoffset().total_seconds() / 60),
        }

    if isinstance(value, date):
        return {"year": value.year, "month": value.month, "day": value.day}

    if isinstance(value, timedelta):
        return value.total_seconds()

    return value


def to_camelcase_dict(value):
    return to_case_dict(value, case=camelcase)


def to_snakecase_dict(value):
    return to_case_dict(value, case=snakecase)
