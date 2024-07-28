import json 

import pytest

from f1.live_data import filter_messages
from f1.live_data import get_pos_1_constructor_color

@pytest.fixture(autouse=True)
def drivers():
    with open("data/drivers.json") as f:
        return json.load(f)

@pytest.mark.parametrize(
    "test_name, msg, expected",
    [
        (
            "Heartbeat message",
            {'Utc': '2024-07-27T10:43:01.0486547Z', '_kf': True},
            None,
        ),
        (
            "DriverList message",
            {'1': {'Line': 1}, '81': {'Line': 4}, '4': {'Line': 6}, '31': {'Line': 10}, '16': {'Line': 8}, '44': {'Line': 3}, '11': {'Line': 2}, '14': {'Line': 9}, '63': {'Line': 5}, '55': {'Line': 7}},
            {'1': {'Line': 1}, '81': {'Line': 4}, '4': {'Line': 6}, '31': {'Line': 10}, '16': {'Line': 8}, '44': {'Line': 3}, '11': {'Line': 2}, '14': {'Line': 9}, '63': {'Line': 5}, '55': {'Line': 7}},
        ),
    ],
)
def test_filter_messages(test_name, msg, expected):
    out = filter_messages(msg)
    assert out == expected

@pytest.mark.parametrize(
    "test_name, driver_list, expected_rgb",
    [
        (
            "DriverList contains position 1 info",
            {'1': {'Line': 1}, '81': {'Line': 4}, '4': {'Line': 6}, '31': {'Line': 10}, '16': {'Line': 8}, '44': {'Line': 3}, '11': {'Line': 2}, '14': {'Line': 9}, '63': {'Line': 5}, '55': {'Line': 7}},
            [54, 113, 198],
        ),
        (
            "DriverList DOES NOT contain position 1 info",
            {'1': {'Line': 10}, '11': {'Line': 9}},
            None,
        ),
    ],
)
def test_pos_1_constructor_color(test_name, driver_list, expected_rgb, drivers):
    out = get_pos_1_constructor_color(driver_list, drivers)
    assert out == expected_rgb
