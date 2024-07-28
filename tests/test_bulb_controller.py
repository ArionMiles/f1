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
            [108, 211, 191],
        ),
        (
            "McLaren",
            [245, 128, 32],
        ),
        (
            "Red Bull",
            [54, 113, 198],
        ),
        (
            "Ferrari",
            [249, 21, 54],
        ),
    ],
)
def test_change_bulb_color(constructor, color, devices):
    # Mercedes
    change_bulb_color(devices, color)
    time.sleep(1)
    for device in devices:
        device.turn_off()
    
