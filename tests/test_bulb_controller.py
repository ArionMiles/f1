import time

import pytest

from f1.bulb_controller import get_devices
from f1.bulb_controller import change_bulb_color

@pytest.fixture(autouse=True)
def devices():
    return get_devices("data/devices.json")

@pytest.mark.parametrize(
    "constructor, color",
    [
        (
            "Mercedes",
            [0, 255, 242],
        ),
        (
            "McLaren",
            [255, 140, 0],
        ),
        (
            "Red Bull",
            [54, 113, 198],
        ),
        (
            "Ferrari",
            [255, 8, 0],
        ),
    ],
)
def test_change_bulb_color(constructor, color, devices):
    # Mercedes
    change_bulb_color(devices, color)
    time.sleep(1)
    for device in devices:
        device.turn_off()
    
