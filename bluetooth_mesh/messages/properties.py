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
# pylint: disable=W0223

# Property IDs available in mesh:
#   "Mesh Device Properties v2"
#   https://www.bluetooth.com/specifications/specs/mesh-device-properties-2/
#
# Format specification:
#   "GATT Specification Supplement v6"
#   https://www.bluetooth.org/docman/handlers/DownloadDoc.ashx?doc_id=539729

from datetime import date, timedelta
from enum import IntEnum
from math import log, pow

from construct import (
    Adapter,
    BitsInteger,
    BytesInteger,
    Embedded,
    ExprAdapter,
    Flag,
    Float32b,
    Int8sl,
    Int8ul,
    Int16sl,
    Int16ul,
    Int24ul,
    Int32ul,
    PaddedString,
    Struct,
    obj_,
)

from bluetooth_mesh.messages.config import EmbeddedBitStruct
from bluetooth_mesh.messages.util import AliasedContainer, DefaultCountValidator, EnumAdapter


class PropertyID(IntEnum):
    AVERAGE_AMBIENT_TEMPERATURE_IN_A_PERIOD_OF_DAY = 0x0001
    AVERAGE_INPUT_CURRENT = 0x0002
    AVERAGE_INPUT_VOLTAGE = 0x0003
    AVERAGE_OUTPUT_CURRENT = 0x0004
    AVERAGE_OUTPUT_VOLTAGE = 0x0005
    CENTER_BEAM_INTENSITY_AT_FULL_POWER = 0x0006
    CHROMATICITY_TOLERANCE = 0x0007
    COLOR_RENDERING_INDEX_R9 = 0x0008
    COLOR_RENDERING_INDEX_RA = 0x0009
    DEVICE_APPEARANCE = 0x000A
    DEVICE_COUNTRY_OF_ORIGIN = 0x000B
    DEVICE_DATE_OF_MANUFACTURE = 0x000C
    DEVICE_ENERGY_USE_SINCE_TURN_ON = 0x000D
    DEVICE_FIRMWARE_REVISION = 0x000E
    DEVICE_GLOBAL_TRADE_ITEM_NUMBER = 0x000F
    DEVICE_HARDWARE_REVISION = 0x0010
    DEVICE_MANUFACTURER_NAME = 0x0011
    DEVICE_MODEL_NUMBER = 0x0012
    DEVICE_OPERATING_TEMPERATURE_RANGE_SPECIFICATION = 0x0013
    DEVICE_OPERATING_TEMPERATURE_STATISTICAL_VALUES = 0x0014
    DEVICE_OVER_TEMPERATURE_EVENT_STATISTICS = 0x0015
    DEVICE_POWER_RANGE_SPECIFICATION = 0x0016
    DEVICE_RUNTIME_SINCE_TURN_ON = 0x0017
    DEVICE_RUNTIME_WARRANTY = 0x0018
    DEVICE_SERIAL_NUMBER = 0x0019
    DEVICE_SOFTWARE_REVISION = 0x001A
    DEVICE_UNDER_TEMPERATURE_EVENT_STATISTICS = 0x001B
    INDOOR_AMBIENT_TEMPERATURE_STATISTICAL_VALUES = 0x001C
    INITIAL_CIE1931_CHROMATICITY_COORDINATES = 0x001D
    INITIAL_CORRELATED_COLOR_TEMPERATURE = 0x001E
    INITIAL_LUMINOUS_FLUX = 0x001F
    INITIAL_PLANCKIAN_DISTANCE = 0x0020
    INPUT_CURRENT_RANGE_SPECIFICATION = 0x0021
    INPUT_CURRENT_STATISTICS = 0x0022
    INPUT_OVER_CURRENT_EVENT_STATISTICS = 0x0023
    INPUT_OVER_RIPPLE_VOLTAGE_EVENT_STATISTICS = 0x0024
    INPUT_OVER_VOLTAGE_EVENT_STATISTICS = 0x0025
    INPUT_UNDER_CURRENT_EVENT_STATISTICS = 0x0026
    INPUT_UNDER_VOLTAGE_EVENT_STATISTICS = 0x0027
    INPUT_VOLTAGE_RANGE_SPECIFICATION = 0x0028
    INPUT_VOLTAGE_RIPPLE_SPECIFICATION = 0x0029
    INPUT_VOLTAGE_STATISTICS = 0x002A
    LIGHT_CONTROL_AMBIENT_LUXLEVEL_ON = 0x002B
    LIGHT_CONTROL_AMBIENT_LUXLEVEL_PROLONG = 0x002C
    LIGHT_CONTROL_AMBIENT_LUXLEVEL_STANDBY = 0x002D
    LIGHT_CONTROL_LIGHTNESS_ON = 0x002E
    LIGHT_CONTROL_LIGHTNESS_PROLONG = 0x002F
    LIGHT_CONTROL_LIGHTNESS_STANDBY = 0x0030
    LIGHT_CONTROL_REGULATOR_ACCURACY = 0x0031
    LIGHT_CONTROL_REGULATOR_KID = 0x0032
    LIGHT_CONTROL_REGULATOR_KIU = 0x0033
    LIGHT_CONTROL_REGULATOR_KPD = 0x0034
    LIGHT_CONTROL_REGULATOR_KPU = 0x0035
    LIGHT_CONTROL_TIME_FADE = 0x0036
    LIGHT_CONTROL_TIME_FADE_ON = 0x0037
    LIGHT_CONTROL_TIME_FADE_STANDBY_AUTO = 0x0038
    LIGHT_CONTROL_TIME_FADE_STANDBY_MANUAL = 0x0039
    LIGHT_CONTROL_TIME_OCCUPANCY_DELAY = 0x003A
    LIGHT_CONTROL_TIME_PROLONG = 0x003B
    LIGHT_CONTROL_TIME_RUN_ON = 0x003C
    LUMEN_MAINTENANCE_FACTOR = 0x003D
    LUMINOUS_EFFICACY = 0x003E
    LUMINOUS_ENERGY_SINCE_TURN_ON = 0x003F
    LUMINOUS_EXPOSURE = 0x0040
    LUMINOUS_FLUX_RANGE = 0x0041
    MOTION_SENSED = 0x0042
    MOTION_THRESHOLD = 0x0043
    OPEN_CIRCUIT_EVENT_STATISTICS = 0x0044
    OUTDOOR_STATISTICAL_VALUES = 0x0045
    OUTPUT_CURRENT_RANGE = 0x0046
    OUTPUT_CURRENT_STATISTICS = 0x0047
    OUTPUT_RIPPLE_VOLTAGE_SPECIFICATION = 0x0048
    OUTPUT_VOLTAGE_RANGE = 0x0049
    OUTPUT_VOLTAGE_STATISTICS = 0x004A
    OVER_OUTPUT_RIPPLE_VOLTAGE_EVENT_STATISTICS = 0x004B
    PEOPLE_COUNT = 0x004C
    PRESENCE_DETECTED = 0x004D
    PRESENT_AMBIENT_LIGHT_LEVEL = 0x004E
    PRESENT_AMBIENT_TEMPERATURE = 0x004F
    PRESENT_CIE1931_CHROMATICITY_COORDINATES = 0x0050
    PRESENT_CORRELATED_COLOR_TEMPERATURE = 0x0051
    PRESENT_DEVICE_INPUT_POWER = 0x0052
    PRESENT_DEVICE_OPERATING_EFFICIENCY = 0x0053
    PRESENT_DEVICE_OPERATING_TEMPERATURE = 0x0054
    PRESENT_ILLUMINANCE = 0x0055
    PRESENT_INDOOR_AMBIENT_TEMPERATURE = 0x0056
    PRESENT_INPUT_CURRENT = 0x0057
    PRESENT_INPUT_RIPPLE_VOLTAGE = 0x0058
    PRESENT_INPUT_VOLTAGE = 0x0059
    PRESENT_LUMINOUS_FLUX = 0x005A
    PRESENT_OUTDOOR_AMBIENT_TEMPERATURE = 0x005B
    PRESENT_OUTPUT_CURRENT = 0x005C
    PRESENT_OUTPUT_VOLTAGE = 0x005D
    PRESENT_PLANCKIAN_DISTANCE = 0x005E
    PRESENT_RELATIVE_OUTPUT_RIPPLE_VOLTAGE = 0x005F
    RELATIVE_DEVICE_ENERGY_USE_IN_A_PERIOD_OF_DAY = 0x0060
    RELATIVE_DEVICE_RUNTIME_IN_A_GENERIC_LEVEL_RANGE = 0x0061
    RELATIVE_EXPOSURE_TIME_IN_AN_ILLUMINANCE_RANGE = 0x0062
    RELATIVE_RUNTIME_IN_A_CORRELATED_COLOR_TEMPERATURE_RANGE = 0x0063
    RELATIVE_RUNTIME_IN_A_DEVICE_OPERATING_TEMPERATURE_RANGE = 0x0064
    RELATIVE_RUNTIME_IN_AN_INPUT_CURRENT_RANGE = 0x0065
    RELATIVE_RUNTIME_IN_AN_INPUT_VOLTAGE_RANGE = 0x0066
    SHORT_CIRCUIT_EVENT_STATISTICS = 0x0067
    TIME_SINCE_MOTION_SENSED = 0x0068
    TIME_SINCE_PRESENCE_DETECTED = 0x0069
    TOTAL_DEVICE_ENERGY_USE = 0x006A
    TOTAL_DEVICE_OFF_ON_CYCLES = 0x006B
    TOTAL_DEVICE_POWER_ON_CYCLES = 0x006C
    TOTAL_DEVICE_POWER_ON_TIME = 0x006D
    TOTAL_DEVICE_RUNTIME = 0x006E
    TOTAL_LIGHT_EXPOSURE_TIME = 0x006F
    TOTAL_LUMINOUS_ENERGY = 0x0070
    PRECISE_TOTAL_DEVICE_ENERGY_USE = 0x0072
    POWER_FACTOR = 0x0073
    ACTIVE_ENERGY_LOAD_SIDE = 0x0080
    ACTIVE_POWER_LOAD_SIDE = 0x0081
    APPARENT_POWER = 0x0084
    APPARENT_ENERGY = 0x0083
    EXTERNAL_SUPPLY_VOLTAGE = 0x0088
    EXTERNAL_SUPPLY_VOLTAGE_FREQUENCY = 0x0089
    LIGHT_DISTRIBUTION = 0x008C
    LIGHT_SOURCE_CURRENT = 0x008D
    LIGHT_SOURCE_ON_TIME_NOT_RESETTABLE = 0x008E
    LIGHT_SOURCE_ON_TIME_RESETTABLE = 0x008F
    LIGHT_SOURCE_OPEN_CIRCUIT_STATISTICS = 0x0090
    LIGHT_SOURCE_OVERALL_FAILURES_STATISTICS = 0x0091
    LIGHT_SOURCE_SHORT_CIRCUIT_STATISTICS = 0x0092
    LIGHT_SOURCE_START_COUNTER_RESETTABLE = 0x0093
    LIGHT_SOURCE_TEMPERATURE = 0x0094
    LIGHT_SOURCE_THERMAL_DERATING_STATISTICS = 0x0095
    LIGHT_SOURCE_THERMAL_SHUTDOWN_STATISTICS = 0x0096
    LIGHT_SOURCE_TOTAL_POWER_ON_CYCLES = 0x0097
    LIGHT_SOURCE_VOLTAGE = 0x0098
    LUMINAIRE_COLOR = 0x0099
    LUMINAIRE_IDENTIFICATION_NUMBER = 0x009A
    LUMINAIRE_MANUFACTURER_GTIN = 0x009B
    LUMINAIRE_NOMINAL_INPUT_POWER = 0x009C
    LUMINAIRE_NOMINAL_MAXIMUM_AC_MAINS_VOLTAGE = 0x009D
    LUMINAIRE_NOMINAL_MINIMUM_AC_MAINS_VOLTAGE = 0x009E
    LUMINAIRE_POWER_AT_MINIMUM_DIM_LEVEL = 0x009F
    LUMINAIRE_TIME_OF_MANUFACTURE = 0x00A0
    NOMINAL_LIGHT_OUTPUT = 0x00A4
    OVERALL_FAILURE_CONDITION = 0x00A5
    RATED_MEDIAN_USEFUL_LIFE_OF_LUMINAIRE = 0x00AB
    RATED_MEDIAN_USEFUL_LIGHT_SOURCE_STARTS = 0x00AC
    REFERENCE_TEMPERATURE = 0x00AD
    TOTAL_DEVICE_STARTS = 0x00AE
    LUMINAIRE_IDENTIFICATION_STRING = 0x00B4
    OUTPUT_POWER_LIMITATION = 0x00B5
    THERMAL_DERATING = 0x00B6
    OUTPUT_CURRENT_PERCENT = 0x00B7
    LIGHT_SOURCE_TYPE = 0x00B3
    SENSOR_GAIN = 0x0074
    PRECISE_PRESENT_AMBIENT_TEMPERATURE = 0x0075
    DESIRED_AMBIENT_TEMPERATURE = 0x0071

    def __repr__(self):
        return str(self.value)


class TimeExponential8Validator(Adapter):
    _subcon = Float32b

    def _decode(self, obj, content, path):
        return round(pow(1.1, obj - 64), 4) if obj else 0

    def _encode(self, obj, content, path):
        return round(log(obj, 1.1)) + 64 if obj else 0


class DateAdapter(Adapter):
    _subcon = Struct(
        "year" / Int16ul,
        "month" / Int8ul,
        "day" / Int8ul,
    )
    EPOCH = date(1970, 1, 1)

    def _decode(self, obj, content, path):
        if obj is None:
            return 0

        return self.EPOCH + timedelta(days=obj)

    def _encode(self, obj, content, path):
        if obj is None:
            return 0

        if isinstance(obj, dict):
            obj = date(obj["year"], obj["month"], obj["day"])

        if isinstance(obj, date):
            return (obj - self.EPOCH).days

        return obj


class LightDistributionField(IntEnum):
    TYPE_NOT_SPECIFIED = 0x00
    TYPE_I = 0x01
    TYPE_II = 0x02
    TYPE_III = 0x03
    TYPE_IV = 0x04
    TYPE_V = 0x05


class LightSourceTypeField(IntEnum):
    TYPE_NOT_SPECIFIED = 0x00
    LOW_PRESSURE_FLUORESCENT = 0x01
    HIGH_INTENSITY_DISCHARGE = 0x02
    LOW_VOLTAGE_HALOGEN = 0x03
    INCANDESCENT = 0x04
    LIGHT_EMITTING_DIODE = 0x05
    ORGANIC_LIGHT_EMITTING_DIODE = 0x06
    OTHER_THAN_LISTED_ABOVE = 0xFD
    NO_LIGHT_SOURCE = 0xFE
    MULTIPLE_LIGHT_SOURCE_TYPES = 0xFF


def FixedString(size):
    def decode_bytes(obj, context):
        return obj.decode() if isinstance(obj, bytes) else obj

    return ExprAdapter(
        PaddedString(size, "utf8"),
        obj_,
        decode_bytes,
    )


# fmt: off


# time
TimeMiliseconds24 = Struct(
    "seconds" / DefaultCountValidator(Int24ul, rounding=3, resolution=0.001)
)

TimeHour24 = Struct(
    "hours" / DefaultCountValidator(Int24ul)
)

TimeSecond16 = Struct(
    "seconds" / DefaultCountValidator(Int16ul)
)

TimeSecond32 = Struct(
    "seconds" / DefaultCountValidator(Int32ul)
)

TimeExponential8 = Struct(
    "seconds" / TimeExponential8Validator(Int8ul)
)

TimeDecihour8 = Struct(
    "hour" / DefaultCountValidator(Int8ul, rounding=1, resolution=0.1)
)

DateUTC = Struct(
    "date" / DateAdapter(Int24ul)
)


# electric current
ElectricCurrent = Struct(
    "current" / DefaultCountValidator(Int16ul, rounding=2, resolution=0.01)
)

AverageCurrent = Struct(
    "electric_current_value" / DefaultCountValidator(Int16ul, rounding=2, resolution=0.01),
    "sensing_duration" / TimeExponential8,
)

ElectricCurrentRange = Struct(
    "minimum_electric_current_value" / DefaultCountValidator(Int16ul, rounding=2, resolution=0.01),
    "maximum_electric_current_value" / DefaultCountValidator(Int16ul, rounding=2, resolution=0.01),
)

ElectricCurrentSpecification = Struct(
    "minimum_electric_current_value" / DefaultCountValidator(Int16ul, rounding=2, resolution=0.01),
    "typical_electric_current_value" / DefaultCountValidator(Int16ul, rounding=2, resolution=0.01),
    "maximum_electric_current_value" / DefaultCountValidator(Int16ul, rounding=2, resolution=0.01),
)

ElectricCurrentStatistics = Struct(
    "average_electric_current_value" / DefaultCountValidator(Int16ul, rounding=2, resolution=0.01),
    "standard_deviation_electric_current_value" / DefaultCountValidator(Int16ul, rounding=2, resolution=0.01),
    Embedded(ElectricCurrentRange),
    "sensing_duration" / TimeExponential8,
)

RelativeValueInACurrentRange = Struct(
    "relative_value" / DefaultCountValidator(Int8ul, rounding=1, resolution=0.5),
    "minimum_current" / DefaultCountValidator(Int16ul, rounding=2, resolution=0.01),
    "maximum_current" / DefaultCountValidator(Int16ul, rounding=2, resolution=0.01)
)


# voltage
Voltage = Struct(
    "voltage" / DefaultCountValidator(Int16ul, resolution=1/64),
)

AverageVoltage = Struct(
    "voltage_value" / DefaultCountValidator(Int16ul, resolution=1/64),
    "sensing_duration" / TimeExponential8,
)

VoltageRange = Struct(
    "minimum_voltage_value" / DefaultCountValidator(Int16ul, resolution=1/64),
    "typical_voltage_value" / DefaultCountValidator(Int16ul, resolution=1/64),
    "maximum_voltage_value" / DefaultCountValidator(Int16ul, resolution=1/64),
)

VoltageStatistics = Struct(
    "average_voltage_value" / DefaultCountValidator(Int16ul, resolution=1/64),
    "standard_deviation_voltage_value" / DefaultCountValidator(Int16ul, resolution=1/64),
    "minimum_voltage_value" / DefaultCountValidator(Int16ul, resolution=1/64),
    "maximum_voltage_value" / DefaultCountValidator(Int16ul, resolution=1/64),
    "sensing_duration" / TimeExponential8,
)

RelativeValueInAVoltageRange = Struct(
    "relative_value" / DefaultCountValidator(Int8ul, rounding=1, resolution=0.5, unknown_value=False),
    "minimum_voltage" / DefaultCountValidator(Int16ul, resolution=1/64),
    "maximum_voltage" / DefaultCountValidator(Int16ul, resolution=1/64),
)

HighVoltage = Struct(
    "high_voltage" / DefaultCountValidator(Int24ul, resolution=1/64, unknown_value=False),
)

VoltageFrequency = Struct(
    "voltage_frequency" / Int16ul
)

# energy
Energy = Struct(
    "energy" / DefaultCountValidator(Int24ul)
)

PreciseEnergy = Struct(
    "energy" / DefaultCountValidator(Int32ul, resolution=0.001, rounding=3, unknown_value=False)
)


EnergyInAPeriodOfDay = Struct(
    "energy_value" / DefaultCountValidator(Int24ul),
    "start_time" / TimeDecihour8,
    "end_time" / TimeDecihour8,
)

ApparentEnergy32 = Struct(
    "energy" / DefaultCountValidator(Int32ul, rounding=3, resolution=0.001, unknown_value=False),
)

Energy32 = Struct(
    "energy" / DefaultCountValidator(Int32ul, rounding=3, resolution=0.001, unknown_value=False),
)


# power
Power = Struct(
    "power" / DefaultCountValidator(Int24ul, rounding=1, resolution=0.1)
)

PowerSpecification = Struct(
    "minimum_power_value" / DefaultCountValidator(Int24ul, rounding=1, resolution=0.1),
    "typical_power_value" / DefaultCountValidator(Int24ul, rounding=1, resolution=0.1),
    "maximum_power_value" / DefaultCountValidator(Int24ul, rounding=1, resolution=0.1)
)

ApparentPower = Struct(
    "power" / DefaultCountValidator(Int24ul, rounding=1, resolution=0.1),
)


# temperature
Temperature = Struct(
    "temperature" / DefaultCountValidator(Int16sl, rounding=2, resolution=0.01)
)

Temperature8 = Struct(
    "temperature" / DefaultCountValidator(Int8sl, rounding=1, resolution=0.5)
)

TemperatureRange = Struct(
    "minimum_temperature" / DefaultCountValidator(Int8sl, rounding=1, resolution=0.5),
    "maximum_temperature" / DefaultCountValidator(Int8sl, rounding=1, resolution=0.5),
)

Temperature8Statistics = Struct(
    "average_temperature" / DefaultCountValidator(Int8sl, rounding=1, resolution=0.5),
    "standard_deviation_temperature" / DefaultCountValidator(Int8sl, rounding=1, resolution=0.5),
    Embedded(TemperatureRange),
    "sensing_duration" / TimeExponential8,
)

Temperature8InAPeriodOfDay = Struct(
    "temperature" / DefaultCountValidator(Int8sl, rounding=1, resolution=0.5),
    "start_time" / TimeDecihour8,
    "end_time" / TimeDecihour8,
)

TemperatureStatistics = Struct(
    "average_temperature" / DefaultCountValidator(Int16sl, rounding=2, resolution=0.01),
    "standard_deviation_temperature" / DefaultCountValidator(Int16sl, rounding=2, resolution=0.01),
    "minimum_temperature" / DefaultCountValidator(Int16sl, rounding=2, resolution=0.01),
    "maximum_temperature" / DefaultCountValidator(Int16sl, rounding=2, resolution=0.01),
    "sensing_duration" / TimeExponential8,
)

HighTemperature = Struct(
    "temperature" / DefaultCountValidator(Int16sl, rounding=1, resolution=0.5, unknown_value=False),
)

RelativeValueInATemperatureRange = Struct(
    "relative_value" / DefaultCountValidator(Int8ul, rounding=1, resolution=0.5, unknown_value=False),
    "minimum_temperature" / DefaultCountValidator(Int16sl, rounding=2, resolution=0.01),
    "maximum_temperature" / DefaultCountValidator(Int16sl, rounding=2, resolution=0.01)
)


# luminosity
LuminousFlux = Struct(
    "luminous_flux" / DefaultCountValidator(Int16ul)
)

LuminousFluxRange = Struct(
    "minimum_luminous_flux" / DefaultCountValidator(Int16ul),
    "maximum_luminous_flux" / DefaultCountValidator(Int16ul)
)

LuminousEnergy = Struct(
    "luminous_energy" / DefaultCountValidator(Int24ul, rounding=1, resolution=1000),
)

LuminousExposure = Struct(
    "luminous_exposure" / DefaultCountValidator(Int24ul, rounding=1, resolution=1000),
)

LuminousIntensity = Struct(
    "luminous_intensity" / DefaultCountValidator(Int16ul)
)

LuminousEfficacy = Struct(
    "luminous_efficacy" / DefaultCountValidator(Int16ul, rounding=1, resolution=0.1)
)

Illuminance = Struct(
    "illuminance" / DefaultCountValidator(Int24ul, rounding=2, resolution=0.01, unknown_value=False)
)

RelativeValueInAnIlluminanceRange = Struct(
    "relative_value" / DefaultCountValidator(Int8ul, rounding=1, resolution=0.5, unknown_value=False),
    "minimum_illuminance" / DefaultCountValidator(Int24ul, rounding=2, resolution=0.01, unknown_value=False),
    "maximum_illuminance" / DefaultCountValidator(Int24ul, rounding=2, resolution=0.01, unknown_value=False)
)

PerceivedLightness = Struct(
    "perceived_lightness" / Int16ul
)

LightDistribution = Struct(
    "light_distribution" / EnumAdapter(Int8ul, LightDistributionField)
)

LightOutput = Struct(
    "light_output" / DefaultCountValidator(Int24ul, rounding=1, resolution=1, unknown_value=False)
)

LightSourceType = Struct(
    "light_source_type" / EnumAdapter(Int8ul, LightSourceTypeField)
)

# counters
Percentage8 = Struct(
    "percentage" / DefaultCountValidator(Int8ul, rounding=1, resolution=0.5)
)

Count16 = Struct(
    "count" / DefaultCountValidator(Int16ul)
)

Count24 = Struct(
    "count" / DefaultCountValidator(Int24ul)
)

Coefficient = Struct(
    "coefficient" / DefaultCountValidator(Int32ul)
)


# chromaticity
ChromaticityTolerance = Struct(
    "chromaticity_tolerance" / DefaultCountValidator(Int8sl, rounding=4, resolution=0.0001, unknown_value=False)
)

ChromaticDistanceFromPlanckian = Struct(
    "distance_from_planckian" / DefaultCountValidator(Int16sl, rounding=5, resolution=0.00001, unknown_value=False)
)

CorrelatedColorTemperature = Struct(
    "correlated_color_temperature" / DefaultCountValidator(Int16ul, rounding=1, resolution=1)
)

ChromaticityCoordinates = Struct(
    "chromaticity_x_coordinate" / DefaultCountValidator(Int16ul, resolution=1/0xffff, unknown_value=False),
    "chromaticity_y_coordinate" / DefaultCountValidator(Int16ul, resolution=1/0xffff, unknown_value=False)
)

ColorRenderingIndex = Struct(
    "color_rendering_index" / DefaultCountValidator(Int8sl, unknown_value=False)
)


# misc
CosineOfTheAngle = Struct(
    "cosine_of_the_angle" / Int8sl
)

GlobalTradeItemNumber = Struct(
    "global_trade_item_number" / BytesInteger(6, swapped=True)
)

Appearance = Struct(  # TODO: check if correct
    *EmbeddedBitStruct(
        "_",
        "category" / BitsInteger(10),
        "sub_category" / BitsInteger(6),
        reversed=True
    )
)

CountryCode = Struct(
    "country_code" / DefaultCountValidator(Int16ul)
)

Presence = Struct(
    "presence_detected" / Flag
)

EventStatistics = Struct(
    "number_of_events" / Count16,
    "average_event_duration" / TimeSecond16,
    "time_elapsed_since_last_event" / TimeExponential8,
    "sensing_duration" / TimeExponential8,
)

RelativeRuntimeInAGenericLevelRange = Struct(
    "relative_value" / DefaultCountValidator(Int8ul, rounding=1, resolution=0.5, unknown_value=False),
    "minimum_generic_level" / DefaultCountValidator(Int16ul, unknown_value=False),
    "maximum_generic_level" / DefaultCountValidator(Int16ul, unknown_value=False),
)

PropertyDict = {
    PropertyID.AVERAGE_AMBIENT_TEMPERATURE_IN_A_PERIOD_OF_DAY: Temperature8InAPeriodOfDay,
    PropertyID.AVERAGE_INPUT_CURRENT: AverageCurrent,
    PropertyID.AVERAGE_INPUT_VOLTAGE: AverageVoltage,
    PropertyID.AVERAGE_OUTPUT_CURRENT: AverageCurrent,
    PropertyID.AVERAGE_OUTPUT_VOLTAGE: AverageVoltage,
    PropertyID.CENTER_BEAM_INTENSITY_AT_FULL_POWER: LuminousIntensity,
    PropertyID.CHROMATICITY_TOLERANCE: ChromaticityTolerance,
    PropertyID.COLOR_RENDERING_INDEX_R9: ColorRenderingIndex,
    PropertyID.COLOR_RENDERING_INDEX_RA: ColorRenderingIndex,
    PropertyID.DEVICE_APPEARANCE: Appearance,
    PropertyID.DEVICE_COUNTRY_OF_ORIGIN: CountryCode,
    PropertyID.DEVICE_DATE_OF_MANUFACTURE: DateUTC,
    PropertyID.DEVICE_ENERGY_USE_SINCE_TURN_ON: Energy,
    PropertyID.DEVICE_FIRMWARE_REVISION: FixedString(8),
    PropertyID.DEVICE_GLOBAL_TRADE_ITEM_NUMBER: GlobalTradeItemNumber,
    PropertyID.DEVICE_HARDWARE_REVISION: FixedString(16),
    PropertyID.DEVICE_MANUFACTURER_NAME: FixedString(36),
    PropertyID.DEVICE_MODEL_NUMBER: FixedString(24),
    PropertyID.DEVICE_OPERATING_TEMPERATURE_RANGE_SPECIFICATION: TemperatureRange,
    PropertyID.DEVICE_OPERATING_TEMPERATURE_STATISTICAL_VALUES: TemperatureStatistics,
    PropertyID.DEVICE_OVER_TEMPERATURE_EVENT_STATISTICS: EventStatistics,
    PropertyID.DEVICE_POWER_RANGE_SPECIFICATION: PowerSpecification,
    PropertyID.DEVICE_RUNTIME_SINCE_TURN_ON: TimeHour24,
    PropertyID.DEVICE_RUNTIME_WARRANTY: TimeHour24,
    PropertyID.DEVICE_SERIAL_NUMBER: FixedString(16),
    PropertyID.DEVICE_SOFTWARE_REVISION: FixedString(8),
    PropertyID.DEVICE_UNDER_TEMPERATURE_EVENT_STATISTICS: EventStatistics,
    PropertyID.INDOOR_AMBIENT_TEMPERATURE_STATISTICAL_VALUES: Temperature8Statistics,
    PropertyID.INITIAL_CIE1931_CHROMATICITY_COORDINATES: ChromaticityCoordinates,
    PropertyID.INITIAL_CORRELATED_COLOR_TEMPERATURE: CorrelatedColorTemperature,
    PropertyID.INITIAL_LUMINOUS_FLUX: LuminousFlux,
    PropertyID.INITIAL_PLANCKIAN_DISTANCE: ChromaticDistanceFromPlanckian,
    PropertyID.INPUT_CURRENT_RANGE_SPECIFICATION: ElectricCurrentSpecification,
    PropertyID.INPUT_CURRENT_STATISTICS: ElectricCurrentStatistics,
    PropertyID.INPUT_OVER_CURRENT_EVENT_STATISTICS: EventStatistics,
    PropertyID.INPUT_OVER_RIPPLE_VOLTAGE_EVENT_STATISTICS: EventStatistics,
    PropertyID.INPUT_OVER_VOLTAGE_EVENT_STATISTICS: EventStatistics,
    PropertyID.INPUT_UNDER_CURRENT_EVENT_STATISTICS: EventStatistics,
    PropertyID.INPUT_UNDER_VOLTAGE_EVENT_STATISTICS: EventStatistics,
    PropertyID.INPUT_VOLTAGE_RANGE_SPECIFICATION: VoltageRange,
    PropertyID.INPUT_VOLTAGE_RIPPLE_SPECIFICATION: Percentage8,
    PropertyID.INPUT_VOLTAGE_STATISTICS: VoltageStatistics,
    PropertyID.LIGHT_CONTROL_AMBIENT_LUXLEVEL_ON: Illuminance,
    PropertyID.LIGHT_CONTROL_AMBIENT_LUXLEVEL_PROLONG: Illuminance,
    PropertyID.LIGHT_CONTROL_AMBIENT_LUXLEVEL_STANDBY: Illuminance,
    PropertyID.LIGHT_CONTROL_LIGHTNESS_ON: PerceivedLightness,
    PropertyID.LIGHT_CONTROL_LIGHTNESS_PROLONG: PerceivedLightness,
    PropertyID.LIGHT_CONTROL_LIGHTNESS_STANDBY: PerceivedLightness,
    PropertyID.LIGHT_CONTROL_REGULATOR_ACCURACY: Percentage8,
    PropertyID.LIGHT_CONTROL_REGULATOR_KID: Coefficient,
    PropertyID.LIGHT_CONTROL_REGULATOR_KIU: Coefficient,
    PropertyID.LIGHT_CONTROL_REGULATOR_KPD: Coefficient,
    PropertyID.LIGHT_CONTROL_REGULATOR_KPU: Coefficient,
    PropertyID.LIGHT_CONTROL_TIME_FADE: TimeMiliseconds24,
    PropertyID.LIGHT_CONTROL_TIME_FADE_ON: TimeMiliseconds24,
    PropertyID.LIGHT_CONTROL_TIME_FADE_STANDBY_AUTO: TimeMiliseconds24,
    PropertyID.LIGHT_CONTROL_TIME_FADE_STANDBY_MANUAL: TimeMiliseconds24,
    PropertyID.LIGHT_CONTROL_TIME_OCCUPANCY_DELAY: TimeMiliseconds24,
    PropertyID.LIGHT_CONTROL_TIME_PROLONG: TimeMiliseconds24,
    PropertyID.LIGHT_CONTROL_TIME_RUN_ON: TimeMiliseconds24,
    PropertyID.LUMEN_MAINTENANCE_FACTOR: Percentage8,
    PropertyID.LUMINOUS_EFFICACY: LuminousEfficacy,
    PropertyID.LUMINOUS_ENERGY_SINCE_TURN_ON: LuminousEnergy,
    PropertyID.LUMINOUS_EXPOSURE: LuminousExposure,
    PropertyID.LUMINOUS_FLUX_RANGE: LuminousFluxRange,
    PropertyID.MOTION_SENSED: Percentage8,
    PropertyID.MOTION_THRESHOLD: Percentage8,
    PropertyID.OPEN_CIRCUIT_EVENT_STATISTICS: EventStatistics,
    PropertyID.OUTDOOR_STATISTICAL_VALUES: Temperature8Statistics,
    PropertyID.OUTPUT_CURRENT_RANGE: ElectricCurrentRange,
    PropertyID.OUTPUT_CURRENT_STATISTICS: ElectricCurrentStatistics,
    PropertyID.OUTPUT_RIPPLE_VOLTAGE_SPECIFICATION: Percentage8,
    PropertyID.OUTPUT_VOLTAGE_RANGE: VoltageRange,
    PropertyID.OUTPUT_VOLTAGE_STATISTICS: VoltageStatistics,
    PropertyID.OVER_OUTPUT_RIPPLE_VOLTAGE_EVENT_STATISTICS: EventStatistics,
    PropertyID.PEOPLE_COUNT: Count16,
    PropertyID.PRESENCE_DETECTED: Presence,
    PropertyID.PRESENT_AMBIENT_LIGHT_LEVEL: Illuminance,
    PropertyID.PRESENT_AMBIENT_TEMPERATURE: Temperature8,
    PropertyID.PRESENT_CIE1931_CHROMATICITY_COORDINATES: ChromaticityCoordinates,
    PropertyID.PRESENT_CORRELATED_COLOR_TEMPERATURE: CorrelatedColorTemperature,
    PropertyID.PRESENT_DEVICE_INPUT_POWER: Power,
    PropertyID.PRESENT_DEVICE_OPERATING_EFFICIENCY: Percentage8,
    PropertyID.PRESENT_DEVICE_OPERATING_TEMPERATURE: Temperature,
    PropertyID.PRESENT_ILLUMINANCE: Illuminance,
    PropertyID.PRESENT_INDOOR_AMBIENT_TEMPERATURE: Temperature8,
    PropertyID.PRESENT_INPUT_CURRENT: ElectricCurrent,
    PropertyID.PRESENT_INPUT_RIPPLE_VOLTAGE: Percentage8,
    PropertyID.PRESENT_INPUT_VOLTAGE: Voltage,
    PropertyID.PRESENT_LUMINOUS_FLUX: LuminousFlux,
    PropertyID.PRESENT_OUTDOOR_AMBIENT_TEMPERATURE: Temperature8,
    PropertyID.PRESENT_OUTPUT_CURRENT: ElectricCurrent,
    PropertyID.PRESENT_OUTPUT_VOLTAGE: Voltage,
    PropertyID.PRESENT_PLANCKIAN_DISTANCE: ChromaticDistanceFromPlanckian,
    PropertyID.PRESENT_RELATIVE_OUTPUT_RIPPLE_VOLTAGE: Percentage8,
    PropertyID.RELATIVE_DEVICE_ENERGY_USE_IN_A_PERIOD_OF_DAY: EnergyInAPeriodOfDay,
    PropertyID.RELATIVE_DEVICE_RUNTIME_IN_A_GENERIC_LEVEL_RANGE: RelativeRuntimeInAGenericLevelRange,
    PropertyID.RELATIVE_EXPOSURE_TIME_IN_AN_ILLUMINANCE_RANGE: RelativeValueInAnIlluminanceRange,
    PropertyID.RELATIVE_RUNTIME_IN_A_CORRELATED_COLOR_TEMPERATURE_RANGE: LuminousEnergy,
    PropertyID.RELATIVE_RUNTIME_IN_A_DEVICE_OPERATING_TEMPERATURE_RANGE: RelativeValueInATemperatureRange,
    PropertyID.RELATIVE_RUNTIME_IN_AN_INPUT_CURRENT_RANGE: RelativeValueInACurrentRange,
    PropertyID.RELATIVE_RUNTIME_IN_AN_INPUT_VOLTAGE_RANGE: RelativeValueInAVoltageRange,
    PropertyID.SHORT_CIRCUIT_EVENT_STATISTICS: EventStatistics,
    PropertyID.TIME_SINCE_MOTION_SENSED: TimeSecond16,
    PropertyID.TIME_SINCE_PRESENCE_DETECTED: TimeSecond16,
    PropertyID.TOTAL_DEVICE_ENERGY_USE: Energy,
    PropertyID.TOTAL_DEVICE_OFF_ON_CYCLES: Count24,
    PropertyID.TOTAL_DEVICE_POWER_ON_CYCLES: Count24,
    PropertyID.TOTAL_DEVICE_POWER_ON_TIME: TimeHour24,
    PropertyID.TOTAL_DEVICE_RUNTIME: TimeHour24,
    PropertyID.TOTAL_LIGHT_EXPOSURE_TIME: TimeHour24,
    PropertyID.TOTAL_LUMINOUS_ENERGY: LuminousEnergy,
    PropertyID.PRECISE_TOTAL_DEVICE_ENERGY_USE: PreciseEnergy,
    PropertyID.POWER_FACTOR: CosineOfTheAngle,
    PropertyID.EXTERNAL_SUPPLY_VOLTAGE: HighVoltage,
    PropertyID.EXTERNAL_SUPPLY_VOLTAGE_FREQUENCY: VoltageFrequency,
    PropertyID.LIGHT_DISTRIBUTION: LightDistribution,
    PropertyID.LIGHT_SOURCE_CURRENT: AverageCurrent,
    PropertyID.LIGHT_SOURCE_ON_TIME_NOT_RESETTABLE: TimeSecond32,
    PropertyID.LIGHT_SOURCE_ON_TIME_RESETTABLE: TimeSecond32,
    PropertyID.LIGHT_SOURCE_OPEN_CIRCUIT_STATISTICS: EventStatistics,
    PropertyID.LIGHT_SOURCE_OVERALL_FAILURES_STATISTICS: EventStatistics,
    PropertyID.LIGHT_SOURCE_SHORT_CIRCUIT_STATISTICS: EventStatistics,
    PropertyID.LIGHT_SOURCE_START_COUNTER_RESETTABLE: Count24,
    PropertyID.LIGHT_SOURCE_TEMPERATURE: HighTemperature,
    PropertyID.LIGHT_SOURCE_THERMAL_DERATING_STATISTICS: EventStatistics,
    PropertyID.LIGHT_SOURCE_THERMAL_SHUTDOWN_STATISTICS: EventStatistics,
    PropertyID.LIGHT_SOURCE_TOTAL_POWER_ON_CYCLES: Count24,
    PropertyID.LIGHT_SOURCE_VOLTAGE: AverageVoltage,
    PropertyID.LUMINAIRE_COLOR: FixedString(24),
    PropertyID.LUMINAIRE_IDENTIFICATION_NUMBER: FixedString(24),
    PropertyID.LUMINAIRE_NOMINAL_INPUT_POWER: Power,
    PropertyID.LUMINAIRE_NOMINAL_MAXIMUM_AC_MAINS_VOLTAGE: Voltage,
    PropertyID.LUMINAIRE_NOMINAL_MINIMUM_AC_MAINS_VOLTAGE: Voltage,
    PropertyID.LUMINAIRE_POWER_AT_MINIMUM_DIM_LEVEL: Power,
    PropertyID.LUMINAIRE_TIME_OF_MANUFACTURE: DateUTC,
    PropertyID.NOMINAL_LIGHT_OUTPUT: LightOutput,
    PropertyID.OVERALL_FAILURE_CONDITION: EventStatistics,
    PropertyID.RATED_MEDIAN_USEFUL_LIFE_OF_LUMINAIRE: TimeHour24,
    PropertyID.RATED_MEDIAN_USEFUL_LIGHT_SOURCE_STARTS: Count24,
    PropertyID.REFERENCE_TEMPERATURE: HighTemperature,
    PropertyID.TOTAL_DEVICE_STARTS: Count24,
    PropertyID.LUMINAIRE_IDENTIFICATION_STRING: FixedString(64),
    PropertyID.OUTPUT_POWER_LIMITATION: EventStatistics,
    PropertyID.THERMAL_DERATING: EventStatistics,
    PropertyID.OUTPUT_CURRENT_PERCENT: Percentage8,
    PropertyID.LUMINAIRE_MANUFACTURER_GTIN: GlobalTradeItemNumber,
    PropertyID.APPARENT_ENERGY: ApparentEnergy32,
    PropertyID.APPARENT_POWER: ApparentPower,
    PropertyID.ACTIVE_ENERGY_LOAD_SIDE: Energy32,
    PropertyID.ACTIVE_POWER_LOAD_SIDE: Power,
    PropertyID.LIGHT_SOURCE_TYPE: LightSourceType,
    PropertyID.DESIRED_AMBIENT_TEMPERATURE: Temperature8,
    PropertyID.SENSOR_GAIN: Coefficient,
    PropertyID.PRECISE_PRESENT_AMBIENT_TEMPERATURE: Temperature,
}



class PropertyMixin:
    ENUM = IntEnum
    DICT = {}
    ID_FIELD = "property_id"
    VALUE_FIELD = "property_value"

    def _parse_property(self, obj, stream, context, path):
        property_id = self.ENUM(obj.pop(self.ID_FIELD))
        property_name = property_id.name.lower()
        property_value = self.DICT[property_id]._parse(stream, context, path)

        class _Container(AliasedContainer):
            ALIAS = property_name
            ORIGINAL = self.VALUE_FIELD

        return _Container({**obj, self.ID_FIELD: property_id, property_name: property_value})

    def _build_property(self, obj, stream, context, path):
        property_id = self.ENUM(obj[self.ID_FIELD])
        property_name = property_id.name.lower()
        property_value = obj.get(property_name)

        self.DICT[property_id]._build(property_value, stream, context, path)

        return obj
