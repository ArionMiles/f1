import json
import logging
import os

import tinytuya

logger = logging.getLogger(__name__)
log_level = os.environ.get("LOG_LEVEL", "INFO")
logger.setLevel(log_level)

def load_data(filepath: str) -> list[dict]:
    with open(filepath) as f:
        return json.load(f)

def get_devices(filepath: str) -> list[tinytuya.BulbDevice]:
    devices = load_data(filepath)
    bulbs = []
    for device in devices:
        b = tinytuya.BulbDevice(
            dev_id=device["id"],
            address="Auto", #device.get("ip", "Auto"),
            local_key=device["key"], 
            version=3.3) # IMPORTANT to set this regardless of version
        b.turn_on()
        # b.set_socketPersistent(True) # Optional: Keep socket open for multiple commands
        logger.debug(b.status())
        bulbs.append(b)
    return bulbs


def change_bulb_color(devices: list[tinytuya.BulbDevice], rgb: list):
    if len(rgb) != 3:
        logger.error("RGB color values must be in a list of length 3")
        return
    for device in devices:
        logger.debug("change_bulb_color fired")
        device.set_colour(*rgb) # nowait = Go fast don't wait for response
