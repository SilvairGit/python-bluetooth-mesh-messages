from datetime import datetime, timedelta, timezone

import pytest

from bluetooth_mesh.messages.silvair.emergency_lighting_test import (
    EmergencyLightingTestParams,
    EmergencyLightingTestProperty,
    EmergencyLightingTestSubOpcode,
    TestExecutionStatus,
)

valid = [
    pytest.param(
        bytes.fromhex("00"),
        EmergencyLightingTestSubOpcode.ELT_FUNCTIONAL_TEST_GET,
        {},
    ),
    pytest.param(
        bytes.fromhex("01"),
        EmergencyLightingTestSubOpcode.ELT_FUNCTIONAL_TEST_START,
        {},
    ),
    pytest.param(
        bytes.fromhex("02"),
        EmergencyLightingTestSubOpcode.ELT_FUNCTIONAL_TEST_STOP,
        {},
    ),
    pytest.param(
        bytes.fromhex(
            "03"  # Subopcode
            "0000000000"  # ELT Test TAI Timestamp: TAI Seconds
            "40"  # ELT Test TAI Timestamp: Time Zone Offset
            "1F01"  # ELT Test TAI Timestamp: TAI-UTC Delta
            "00"  # ELT Test Execution Status
            "00"  # ELT Test Execution Result
        ),
        EmergencyLightingTestSubOpcode.ELT_FUNCTIONAL_TEST_STATUS,
        dict(
            tai_timestamp=dict(
                date=datetime(
                    1999,
                    12,
                    31,
                    23,
                    59,
                    28,
                    tzinfo=timezone(timedelta(hours=0)),
                ),
                tai_utc_delta=timedelta(seconds=32),
            ),
            execution_result=dict(
                lamp_fault=False,
                battery_fault=False,
                circuit_fault=False,
                battery_duration_fault=False,
            ),
            execution_status=TestExecutionStatus.FINISHED,
        ),
    ),
    pytest.param(
        bytes.fromhex(
            "03"  # Subopcode
            "0000000000"  # ELT Test TAI Timestamp: TAI Seconds
            "40"  # ELT Test TAI Timestamp: Time Zone Offset
            "FF00"  # ELT Test TAI Timestamp: TAI-UTC Delta
            "07"  # ELT Test Execution Status
            "01"  # ELT Test Execution Result
        ),
        EmergencyLightingTestSubOpcode.ELT_FUNCTIONAL_TEST_STATUS,
        dict(
            tai_timestamp=dict(
                date=datetime(
                    2000,
                    1,
                    1,
                    0,
                    0,
                    0,
                    tzinfo=timezone(timedelta(hours=0)),
                ),
                tai_utc_delta=timedelta(seconds=0),
            ),
            execution_result=dict(
                lamp_fault=True,
                battery_fault=False,
                circuit_fault=False,
                battery_duration_fault=False,
            ),
            execution_status=TestExecutionStatus.UNKNOWN,
        ),
    ),
    pytest.param(
        bytes.fromhex(
            "03"  # Subopcode
            "2E48D52F00"  # ELT Test TAI Timestamp: TAI Seconds
            "48"  # ELT Test TAI Timestamp: Time Zone Offset
            "2401"  # ELT Test TAI Timestamp: TAI-UTC Delta
            "02"  # ELT Test Execution Status
            "02"  # ELT Test Execution Result
        ),
        EmergencyLightingTestSubOpcode.ELT_FUNCTIONAL_TEST_STATUS,
        dict(
            tai_timestamp=dict(
                date=datetime(
                    2025,
                    6,
                    6,
                    8,
                    32,
                    41,
                    tzinfo=timezone(timedelta(hours=2)),
                ),
                tai_utc_delta=timedelta(seconds=37),
            ),
            execution_result=dict(
                lamp_fault=False,
                battery_fault=True,
                circuit_fault=False,
                battery_duration_fault=False,
            ),
            execution_status=TestExecutionStatus.IN_PROGRESS,
        ),
    ),
    pytest.param(
        bytes.fromhex(
            "03"  # Subopcode
            "0000000000"  # ELT Test TAI Timestamp: TAI Seconds
            "78"  # ELT Test TAI Timestamp: Time Zone Offset
            "2401"  # ELT Test TAI Timestamp: TAI-UTC Delta
            "03"  # ELT Test Execution Status
            "07"  # ELT Test Execution Result
            "45000000"  # ELT Test Relative Timestamp (optional)
        ),
        EmergencyLightingTestSubOpcode.ELT_FUNCTIONAL_TEST_STATUS,
        dict(
            tai_timestamp=dict(
                date=datetime(
                    2000,
                    1,
                    1,
                    13,
                    59,
                    23,
                    tzinfo=timezone(timedelta(hours=14)),
                ),
                tai_utc_delta=timedelta(seconds=37),
            ),
            execution_result=dict(
                lamp_fault=True,
                battery_fault=True,
                circuit_fault=True,
                battery_duration_fault=False,
            ),
            execution_status=TestExecutionStatus.POSTPONED,
            relative_timestamp=69,
        ),
    ),
    pytest.param(
        bytes.fromhex("04"),
        EmergencyLightingTestSubOpcode.ELT_DURATION_TEST_GET,
        {},
    ),
    pytest.param(
        bytes.fromhex("05"),
        EmergencyLightingTestSubOpcode.ELT_DURATION_TEST_START,
        {},
    ),
    pytest.param(
        bytes.fromhex("06"),
        EmergencyLightingTestSubOpcode.ELT_DURATION_TEST_STOP,
        {},
    ),
    pytest.param(
        bytes.fromhex(
            "07"  # Subopcode
            "0000000000"  # ELT Test TAI Timestamp: TAI Seconds
            "40"  # ELT Test TAI Timestamp: Time Zone Offset
            "1F01"  # ELT Test TAI Timestamp: TAI-UTC Delta
            "00"  # ELT Test Execution Status
            "00"  # ELT Test Execution Result
            "0000"  # ELT Duration Result
        ),
        EmergencyLightingTestSubOpcode.ELT_DURATION_TEST_STATUS,
        dict(
            tai_timestamp=dict(
                date=datetime(
                    1999,
                    12,
                    31,
                    23,
                    59,
                    28,
                    tzinfo=timezone(timedelta(hours=0)),
                ),
                tai_utc_delta=timedelta(seconds=32),
            ),
            execution_result=dict(
                lamp_fault=False,
                battery_fault=False,
                circuit_fault=False,
                battery_duration_fault=False,
            ),
            execution_status=TestExecutionStatus.FINISHED,
            duration_result=0,
        ),
    ),
    pytest.param(
        bytes.fromhex(
            "07"  # Subopcode
            "0000000000"  # ELT Test TAI Timestamp: TAI Seconds
            "40"  # ELT Test TAI Timestamp: Time Zone Offset
            "FF00"  # ELT Test TAI Timestamp: TAI-UTC Delta
            "07"  # ELT Test Execution Status
            "01"  # ELT Test Execution Result
            "FFFF"  # ELT Duration Result
        ),
        EmergencyLightingTestSubOpcode.ELT_DURATION_TEST_STATUS,
        dict(
            tai_timestamp=dict(
                date=datetime(
                    2000,
                    1,
                    1,
                    0,
                    0,
                    0,
                    tzinfo=timezone(timedelta(hours=0)),
                ),
                tai_utc_delta=timedelta(seconds=0),
            ),
            execution_result=dict(
                lamp_fault=True,
                battery_fault=False,
                circuit_fault=False,
                battery_duration_fault=False,
            ),
            execution_status=TestExecutionStatus.UNKNOWN,
            duration_result=65535,
        ),
    ),
    pytest.param(
        bytes.fromhex(
            "07"  # Subopcode
            "2E48D52F00"  # ELT Test TAI Timestamp: TAI Seconds
            "48"  # ELT Test TAI Timestamp: Time Zone Offset
            "2401"  # ELT Test TAI Timestamp: TAI-UTC Delta
            "02"  # ELT Test Execution Status
            "02"  # ELT Test Execution Result
            "0000"  # ELT Duration Result
        ),
        EmergencyLightingTestSubOpcode.ELT_DURATION_TEST_STATUS,
        dict(
            tai_timestamp=dict(
                date=datetime(
                    2025,
                    6,
                    6,
                    8,
                    32,
                    41,
                    tzinfo=timezone(timedelta(hours=2)),
                ),
                tai_utc_delta=timedelta(seconds=37),
            ),
            execution_result=dict(
                lamp_fault=False,
                battery_fault=True,
                circuit_fault=False,
                battery_duration_fault=False,
            ),
            execution_status=TestExecutionStatus.IN_PROGRESS,
            duration_result=0,
        ),
    ),
    pytest.param(
        bytes.fromhex(
            "07"  # Subopcode
            "0000000000"  # ELT Test TAI Timestamp: TAI Seconds
            "78"  # ELT Test TAI Timestamp: Time Zone Offset
            "2401"  # ELT Test TAI Timestamp: TAI-UTC Delta
            "03"  # ELT Test Execution Status
            "0F"  # ELT Test Execution Result
            "100E"  # ELT Duration Result
            "45000000"  # ELT Test Relative Timestamp (optional)
        ),
        EmergencyLightingTestSubOpcode.ELT_DURATION_TEST_STATUS,
        dict(
            tai_timestamp=dict(
                date=datetime(
                    2000,
                    1,
                    1,
                    13,
                    59,
                    23,
                    tzinfo=timezone(timedelta(hours=14)),
                ),
                tai_utc_delta=timedelta(seconds=37),
            ),
            execution_result=dict(
                lamp_fault=True,
                battery_fault=True,
                circuit_fault=True,
                battery_duration_fault=True,
            ),
            execution_status=TestExecutionStatus.POSTPONED,
            duration_result=3600,
            relative_timestamp=69,
        ),
    ),
    pytest.param(
        bytes.fromhex("0884FF"),
        EmergencyLightingTestSubOpcode.ELT_PROPERTY_GET,
        dict(
            property_id=EmergencyLightingTestProperty.ELT_DURATION_TEST_EXECUTION_TIMEOUT,
        ),
    ),
    pytest.param(
        bytes.fromhex("0885FF"),
        EmergencyLightingTestSubOpcode.ELT_PROPERTY_GET,
        dict(
            property_id=EmergencyLightingTestProperty.ELT_FUNCTIONAL_TEST_EXECUTION_TIMEOUT,
        ),
    ),
    pytest.param(
        bytes.fromhex("0886FF"),
        EmergencyLightingTestSubOpcode.ELT_PROPERTY_GET,
        dict(
            property_id=EmergencyLightingTestProperty.ELT_DURATION_TEST_RETRY_PERIOD,
        ),
    ),
    pytest.param(
        bytes.fromhex("0887FF"),
        EmergencyLightingTestSubOpcode.ELT_PROPERTY_GET,
        dict(
            property_id=EmergencyLightingTestProperty.ELT_FUNCTIONAL_TEST_RETRY_PERIOD,
        ),
    ),
    pytest.param(
        bytes.fromhex("0888FF"),
        EmergencyLightingTestSubOpcode.ELT_PROPERTY_GET,
        dict(
            property_id=EmergencyLightingTestProperty.ELT_DURATION_TEST_BACKUP_AUTOMATIC_DELAY,
        ),
    ),
    pytest.param(
        bytes.fromhex("0889FF"),
        EmergencyLightingTestSubOpcode.ELT_PROPERTY_GET,
        dict(
            property_id=EmergencyLightingTestProperty.ELT_FUNCTIONAL_TEST_BACKUP_AUTOMATIC_DELAY,
        ),
    ),
    pytest.param(
        bytes.fromhex("088AFF"),
        EmergencyLightingTestSubOpcode.ELT_PROPERTY_GET,
        dict(
            property_id=EmergencyLightingTestProperty.ELT_DURATION_TEST_BACKUP_AUTOMATIC_INTERVAL,
        ),
    ),
    pytest.param(
        bytes.fromhex("088BFF"),
        EmergencyLightingTestSubOpcode.ELT_PROPERTY_GET,
        dict(
            property_id=EmergencyLightingTestProperty.ELT_FUNCTIONAL_TEST_BACKUP_AUTOMATIC_INTERVAL,
        ),
    ),
    pytest.param(
        bytes.fromhex("0984FF04030201"),
        EmergencyLightingTestSubOpcode.ELT_PROPERTY_SET,
        dict(
            property_id=EmergencyLightingTestProperty.ELT_DURATION_TEST_EXECUTION_TIMEOUT,
            elt_duration_test_execution_timeout=dict(seconds=0x01020304),
        ),
    ),
    pytest.param(
        bytes.fromhex("0985FF04030201"),
        EmergencyLightingTestSubOpcode.ELT_PROPERTY_SET,
        dict(
            property_id=EmergencyLightingTestProperty.ELT_FUNCTIONAL_TEST_EXECUTION_TIMEOUT,
            elt_functional_test_execution_timeout=dict(seconds=0x01020304),
        ),
    ),
    pytest.param(
        bytes.fromhex("0986FF04030201"),
        EmergencyLightingTestSubOpcode.ELT_PROPERTY_SET,
        dict(
            property_id=EmergencyLightingTestProperty.ELT_DURATION_TEST_RETRY_PERIOD,
            elt_duration_test_retry_period=dict(seconds=0x01020304),
        ),
    ),
    pytest.param(
        bytes.fromhex("0987FF04030201"),
        EmergencyLightingTestSubOpcode.ELT_PROPERTY_SET,
        dict(
            property_id=EmergencyLightingTestProperty.ELT_FUNCTIONAL_TEST_RETRY_PERIOD,
            elt_functional_test_retry_period=dict(seconds=0x01020304),
        ),
    ),
    pytest.param(
        bytes.fromhex("0988FF04030201"),
        EmergencyLightingTestSubOpcode.ELT_PROPERTY_SET,
        dict(
            property_id=EmergencyLightingTestProperty.ELT_DURATION_TEST_BACKUP_AUTOMATIC_DELAY,
            elt_duration_test_backup_automatic_delay=dict(seconds=0x01020304),
        ),
    ),
    pytest.param(
        bytes.fromhex("0989FF04030201"),
        EmergencyLightingTestSubOpcode.ELT_PROPERTY_SET,
        dict(
            property_id=EmergencyLightingTestProperty.ELT_FUNCTIONAL_TEST_BACKUP_AUTOMATIC_DELAY,
            elt_functional_test_backup_automatic_delay=dict(seconds=0x01020304),
        ),
    ),
    pytest.param(
        bytes.fromhex("098AFF04030201"),
        EmergencyLightingTestSubOpcode.ELT_PROPERTY_SET,
        dict(
            property_id=EmergencyLightingTestProperty.ELT_DURATION_TEST_BACKUP_AUTOMATIC_INTERVAL,
            elt_duration_test_backup_automatic_interval=dict(seconds=0x01020304),
        ),
    ),
    pytest.param(
        bytes.fromhex("098BFF04030201"),
        EmergencyLightingTestSubOpcode.ELT_PROPERTY_SET,
        dict(
            property_id=EmergencyLightingTestProperty.ELT_FUNCTIONAL_TEST_BACKUP_AUTOMATIC_INTERVAL,
            elt_functional_test_backup_automatic_interval=dict(seconds=0x01020304),
        ),
    ),
    pytest.param(
        bytes.fromhex("0A84FF04030201"),
        EmergencyLightingTestSubOpcode.ELT_PROPERTY_SET_UNACKNOWLEDGED,
        dict(
            property_id=EmergencyLightingTestProperty.ELT_DURATION_TEST_EXECUTION_TIMEOUT,
            elt_duration_test_execution_timeout=dict(seconds=0x01020304),
        ),
    ),
    pytest.param(
        bytes.fromhex("0A85FF04030201"),
        EmergencyLightingTestSubOpcode.ELT_PROPERTY_SET_UNACKNOWLEDGED,
        dict(
            property_id=EmergencyLightingTestProperty.ELT_FUNCTIONAL_TEST_EXECUTION_TIMEOUT,
            elt_functional_test_execution_timeout=dict(seconds=0x01020304),
        ),
    ),
    pytest.param(
        bytes.fromhex("0A86FF04030201"),
        EmergencyLightingTestSubOpcode.ELT_PROPERTY_SET_UNACKNOWLEDGED,
        dict(
            property_id=EmergencyLightingTestProperty.ELT_DURATION_TEST_RETRY_PERIOD,
            elt_duration_test_retry_period=dict(seconds=0x01020304),
        ),
    ),
    pytest.param(
        bytes.fromhex("0A87FF04030201"),
        EmergencyLightingTestSubOpcode.ELT_PROPERTY_SET_UNACKNOWLEDGED,
        dict(
            property_id=EmergencyLightingTestProperty.ELT_FUNCTIONAL_TEST_RETRY_PERIOD,
            elt_functional_test_retry_period=dict(seconds=0x01020304),
        ),
    ),
    pytest.param(
        bytes.fromhex("0A88FF04030201"),
        EmergencyLightingTestSubOpcode.ELT_PROPERTY_SET_UNACKNOWLEDGED,
        dict(
            property_id=EmergencyLightingTestProperty.ELT_DURATION_TEST_BACKUP_AUTOMATIC_DELAY,
            elt_duration_test_backup_automatic_delay=dict(seconds=0x01020304),
        ),
    ),
    pytest.param(
        bytes.fromhex("0A89FF04030201"),
        EmergencyLightingTestSubOpcode.ELT_PROPERTY_SET_UNACKNOWLEDGED,
        dict(
            property_id=EmergencyLightingTestProperty.ELT_FUNCTIONAL_TEST_BACKUP_AUTOMATIC_DELAY,
            elt_functional_test_backup_automatic_delay=dict(seconds=0x01020304),
        ),
    ),
    pytest.param(
        bytes.fromhex("0A8AFF04030201"),
        EmergencyLightingTestSubOpcode.ELT_PROPERTY_SET_UNACKNOWLEDGED,
        dict(
            property_id=EmergencyLightingTestProperty.ELT_DURATION_TEST_BACKUP_AUTOMATIC_INTERVAL,
            elt_duration_test_backup_automatic_interval=dict(seconds=0x01020304),
        ),
    ),
    pytest.param(
        bytes.fromhex("0A8BFF04030201"),
        EmergencyLightingTestSubOpcode.ELT_PROPERTY_SET_UNACKNOWLEDGED,
        dict(
            property_id=EmergencyLightingTestProperty.ELT_FUNCTIONAL_TEST_BACKUP_AUTOMATIC_INTERVAL,
            elt_functional_test_backup_automatic_interval=dict(seconds=0x01020304),
        ),
    ),
    pytest.param(
        bytes.fromhex("0B84FF04030201"),
        EmergencyLightingTestSubOpcode.ELT_PROPERTY_STATUS,
        dict(
            property_id=EmergencyLightingTestProperty.ELT_DURATION_TEST_EXECUTION_TIMEOUT,
            elt_duration_test_execution_timeout=dict(seconds=0x01020304),
        ),
    ),
    pytest.param(
        bytes.fromhex("0B85FF04030201"),
        EmergencyLightingTestSubOpcode.ELT_PROPERTY_STATUS,
        dict(
            property_id=EmergencyLightingTestProperty.ELT_FUNCTIONAL_TEST_EXECUTION_TIMEOUT,
            elt_functional_test_execution_timeout=dict(seconds=0x01020304),
        ),
    ),
    pytest.param(
        bytes.fromhex("0B86FF04030201"),
        EmergencyLightingTestSubOpcode.ELT_PROPERTY_STATUS,
        dict(
            property_id=EmergencyLightingTestProperty.ELT_DURATION_TEST_RETRY_PERIOD,
            elt_duration_test_retry_period=dict(seconds=0x01020304),
        ),
    ),
    pytest.param(
        bytes.fromhex("0B87FF04030201"),
        EmergencyLightingTestSubOpcode.ELT_PROPERTY_STATUS,
        dict(
            property_id=EmergencyLightingTestProperty.ELT_FUNCTIONAL_TEST_RETRY_PERIOD,
            elt_functional_test_retry_period=dict(seconds=0x01020304),
        ),
    ),
    pytest.param(
        bytes.fromhex("0B88FF04030201"),
        EmergencyLightingTestSubOpcode.ELT_PROPERTY_STATUS,
        dict(
            property_id=EmergencyLightingTestProperty.ELT_DURATION_TEST_BACKUP_AUTOMATIC_DELAY,
            elt_duration_test_backup_automatic_delay=dict(seconds=0x01020304),
        ),
    ),
    pytest.param(
        bytes.fromhex("0B89FF04030201"),
        EmergencyLightingTestSubOpcode.ELT_PROPERTY_STATUS,
        dict(
            property_id=EmergencyLightingTestProperty.ELT_FUNCTIONAL_TEST_BACKUP_AUTOMATIC_DELAY,
            elt_functional_test_backup_automatic_delay=dict(seconds=0x01020304),
        ),
    ),
    pytest.param(
        bytes.fromhex("0B8AFF04030201"),
        EmergencyLightingTestSubOpcode.ELT_PROPERTY_STATUS,
        dict(
            property_id=EmergencyLightingTestProperty.ELT_DURATION_TEST_BACKUP_AUTOMATIC_INTERVAL,
            elt_duration_test_backup_automatic_interval=dict(seconds=0x01020304),
        ),
    ),
    pytest.param(
        bytes.fromhex("0B8BFF04030201"),
        EmergencyLightingTestSubOpcode.ELT_PROPERTY_STATUS,
        dict(
            property_id=EmergencyLightingTestProperty.ELT_FUNCTIONAL_TEST_BACKUP_AUTOMATIC_INTERVAL,
            elt_functional_test_backup_automatic_interval=dict(seconds=0x01020304),
        ),
    ),
]


@pytest.mark.parametrize("encoded, subopcode, payload", valid)
def test_parse(encoded, subopcode, payload):
    decoded = EmergencyLightingTestParams.parse(encoded)
    assert decoded.subopcode == subopcode
    assert decoded.payload == payload


@pytest.mark.parametrize("encoded, subopcode, payload", valid)
def test_build(encoded, subopcode, payload):
    assert EmergencyLightingTestParams.build(dict(subopcode=subopcode, payload=payload)) == encoded
