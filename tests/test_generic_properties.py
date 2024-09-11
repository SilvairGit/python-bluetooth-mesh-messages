import pytest

from bluetooth_mesh.messages.generic.property import GenericPropertyMessage, GenericPropertyOpcode
from bluetooth_mesh.messages.properties import LightDistributionField, PropertyID
from bluetooth_mesh.messages.sensor import SensorSettingAccess

valid = [
    # fmt: off
    pytest.param(
        b'\x82\x2E',
        GenericPropertyOpcode.GENERIC_USER_PROPERTIES_GET,
        dict(),
        id="GENERIC_USER_PROPERTIES_GET"),
    pytest.param(
        b'\x4B\x8C\x00\x04\x00\x09\x00',
        GenericPropertyOpcode.GENERIC_USER_PROPERTIES_STATUS,
        dict(property_ids=[PropertyID.LIGHT_DISTRIBUTION,
                           PropertyID.AVERAGE_OUTPUT_CURRENT,
                           PropertyID.COLOR_RENDERING_INDEX_RA]),
        id="GENERIC_USER_PROPERTIES_STATUS"),
    pytest.param(
        b'\x82\x2F\x8C\x00',
        GenericPropertyOpcode.GENERIC_USER_PROPERTY_GET,
        dict(property_id=PropertyID.LIGHT_DISTRIBUTION),
        id="GENERIC_USER_PROPERTY_GET"),
    pytest.param(
        b'\x4C\x8C\x00\x05',
        GenericPropertyOpcode.GENERIC_USER_PROPERTY_SET,
        dict(property_id=PropertyID.LIGHT_DISTRIBUTION,
             light_distribution=dict(
                 light_distribution=LightDistributionField.TYPE_V)),
        id="GENERIC_USER_PROPERTY_SET"),
    pytest.param(
        b'\x4D\x8C\x00\x05',
        GenericPropertyOpcode.GENERIC_USER_PROPERTY_SET_UNACKNOWLEDGED,
        dict(property_id=PropertyID.LIGHT_DISTRIBUTION,
             light_distribution=dict(
                 light_distribution=LightDistributionField.TYPE_V)),
        id="GENERIC_USER_PROPERTY_SET_UNACKNOWLEDGED"),
    pytest.param(
        b'\x4E\x8C\x00\x01\x05',
        GenericPropertyOpcode.GENERIC_USER_PROPERTY_STATUS,
        dict(property_id=PropertyID.LIGHT_DISTRIBUTION,
             access=SensorSettingAccess.READ_ONLY,
             light_distribution=dict(
                 light_distribution=LightDistributionField.TYPE_V)),
        id="GENERIC_USER_PROPERTY_STATUS"),
    pytest.param(
        b'\x82\x2C',
        GenericPropertyOpcode.GENERIC_ADMIN_PROPERTIES_GET,
        dict(),
        id="GENERIC_ADMIN_PROPERTIES_GET"),
    pytest.param(
        b'\x47\x8C\x00\xA4\x00\xB6\x00\xAB\x00',
        GenericPropertyOpcode.GENERIC_ADMIN_PROPERTIES_STATUS,
        dict(property_ids=[PropertyID.LIGHT_DISTRIBUTION,
                           PropertyID.NOMINAL_LIGHT_OUTPUT,
                           PropertyID.THERMAL_DERATING,
                           PropertyID.RATED_MEDIAN_USEFUL_LIFE_OF_LUMINAIRE]
             ),
        id="GENERIC_ADMIN_PROPERTIES_STATUS"),
    pytest.param(
        b'\x82\x2D\x8C\x00',
        GenericPropertyOpcode.GENERIC_ADMIN_PROPERTY_GET,
        dict(property_id=PropertyID.LIGHT_DISTRIBUTION),
        id="GENERIC_ADMIN_PROPERTY_GET"),
    pytest.param(
        b'\x48\x94\x00\x01\x80',
        GenericPropertyOpcode.GENERIC_ADMIN_PROPERTY_SET,
        dict(property_id=PropertyID.LIGHT_SOURCE_TEMPERATURE,
             light_source_temperature=dict(
                 temperature=-16383.5)),  # It supposed to be value not know
        id="GENERIC_ADMIN_PROPERTY_SET"),
    pytest.param(
        b'\x49\xA4\x00\xFF\xFF\xFF',
        GenericPropertyOpcode.GENERIC_ADMIN_PROPERTY_SET_UNACKNOWLEDGED,
        dict(property_id=PropertyID.NOMINAL_LIGHT_OUTPUT,
             nominal_light_output=dict(
                 light_output=16777215)), # It supposed to be value not know
        id="GENERIC_ADMIN_PROPERTY_SET_UNACKNOWLEDGED"),
    pytest.param(
        b'\x4A\xA4\x00\x01\x0A\x00\x00',
        GenericPropertyOpcode.GENERIC_ADMIN_PROPERTY_STATUS,
        dict(property_id=PropertyID.NOMINAL_LIGHT_OUTPUT,
             access=SensorSettingAccess.READ_ONLY,
             nominal_light_output=dict(
                 light_output=10)),
        id="GENERIC_ADMIN_PROPERTY_STATUS"),
    pytest.param(
        b'\x82\x2A',
        GenericPropertyOpcode.GENERIC_MANUFACTURER_PROPERTIES_GET,
        dict(),
        id="GENERIC_MANUFACTURER_PROPERTIES_GET"),
    pytest.param(
        b'\x43\x9d\x00\x8F\x00\xB6\x00\x07\x00',
        GenericPropertyOpcode.GENERIC_MANUFACTURER_PROPERTIES_STATUS,
        dict(property_ids=[PropertyID.LUMINAIRE_NOMINAL_MAXIMUM_AC_MAINS_VOLTAGE,
                           PropertyID.LIGHT_SOURCE_ON_TIME_RESETTABLE,
                           PropertyID.THERMAL_DERATING,
                           PropertyID.CHROMATICITY_TOLERANCE]
             ),
        id="GENERIC_MANUFACTURER_PROPERTIES_STATUS"),
    pytest.param(
        b'\x82\x2D\xA0\x00',
        GenericPropertyOpcode.GENERIC_MANUFACTURER_PROPERTY_GET,
        dict(property_id=PropertyID.LUMINAIRE_TIME_OF_MANUFACTURE),
        id="GENERIC_MANUFACTURER_PROPERTY_GET"),
    pytest.param(
        b'\x44\x73\x00\xE2',
        GenericPropertyOpcode.GENERIC_MANUFACTURER_PROPERTY_SET,
        dict(property_id=PropertyID.POWER_FACTOR,
             power_factor=dict(
                 cosine_of_the_angle=-30)),
        id="GENERIC_MANUFACTURER_PROPERTY_SET"),
    pytest.param(
        b'\x45\x89\x00\xFF\xFF',
        GenericPropertyOpcode.GENERIC_MANUFACTURER_PROPERTY_SET_UNACKNOWLEDGED,
        dict(property_id=PropertyID.EXTERNAL_SUPPLY_VOLTAGE_FREQUENCY,
             external_supply_voltage_frequency=dict(
                 voltage_frequency=65535)), # It supposed to be value not know
        id="GENERIC_MANUFACTURER_PROPERTY_SET_UNACKNOWLEDGED"),
    pytest.param(
        b'\x46\x9A\x00\x01abcdefghijklmnoprstuvxyz',
        GenericPropertyOpcode.GENERIC_MANUFACTURER_PROPERTY_STATUS,
        dict(property_id=PropertyID.LUMINAIRE_IDENTIFICATION_NUMBER,
             access=SensorSettingAccess.READ_ONLY,
             luminaire_identification_number="abcdefghijklmnoprstuvxyz"),
        id="GENERIC_MANUFACTURER_PROPERTY_STATUS"),

    pytest.param(
        b'\x4F',
        GenericPropertyOpcode.GENERIC_CLIENT_PROPERTIES_GET,
        dict(),
        id="GENERIC_CLIENT_PROPERTIES_GET"),
    pytest.param(
        b'\x50\x9d\x00\x8F\x00\xB6\x00\x07\x00',
        GenericPropertyOpcode.GENERIC_CLIENT_PROPERTIES_STATUS,
        dict(property_ids=[PropertyID.LUMINAIRE_NOMINAL_MAXIMUM_AC_MAINS_VOLTAGE,
                           PropertyID.LIGHT_SOURCE_ON_TIME_RESETTABLE,
                           PropertyID.THERMAL_DERATING,
                           PropertyID.CHROMATICITY_TOLERANCE]
             ),
        id="GENERIC_MANUFACTURER_PROPERTIES_STATUS"),
]


@pytest.mark.parametrize("encoded,opcode,data", valid)
def test_parse_valid(encoded, opcode, data):
    assert GenericPropertyMessage.parse(encoded).params == data