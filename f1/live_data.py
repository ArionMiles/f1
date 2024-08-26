import asyncio
from functools import partial
import json
import time
import types
import logging
import os

from fastf1.utils import to_datetime
from fastf1.livetiming.client import SignalRClient
import tinytuya.BulbDevice

from f1.bulb_controller import change_bulb_color

logger = logging.getLogger(__name__)
log_level = os.environ.get("LOG_LEVEL", "INFO")
logger.setLevel(log_level)

def fix_json(line):
    # fix non-compliant JSON data from F1
    line = line.replace("'", '"') \
        .replace('True', 'true') \
        .replace('False', 'false')
    return line

def filter_messages(msg: dict):
    logger.debug("Received: %s", msg)
    # msg with _kf is heartbeat
    if "_kf" not in msg:
        return msg
    logger.info("Received heartbeat: %s", msg)

def get_pos_1_constructor_color(driver_list, drivers):
    for driver_no, position in driver_list.items():
        if not isinstance(position, dict):
            return
        if position["Line"] == 1:
            logger.debug("P1: %s [%s]", drivers[driver_no]["Constructor"], drivers[driver_no]["Name"])
            return drivers[driver_no]["RGB"]

def _to_file_overwrite(devices, drivers, self, msg):
    msg = fix_json(msg)
    try:
        cat, msg, dt = json.loads(msg)
    except (json.JSONDecodeError, ValueError):
        logger.debug(msg)
        logger.warning("JSON parse error")
        return

    filtered_msg = filter_messages(msg)
    if not filtered_msg:
        return
    rgb = get_pos_1_constructor_color(filtered_msg, drivers)
    if rgb:
        logger.info("Changing color"),
        change_bulb_color(devices, rgb)


def _start_overwrite(self):
    """Connect to the data stream and start writing the data."""
    try:
        asyncio.run(self._async_start())
    except KeyboardInterrupt:
        self.logger.warning("Keyboard interrupt - exiting...")
        raise KeyboardInterrupt


def runner(devices: list[tinytuya.BulbDevice], drivers: list):
    client = SignalRClient("unused.txt")
    client.topics = ["Heartbeat", "DriverList"]
    overwrite = partial(_to_file_overwrite, devices, drivers)
    # Override the default file writer to send events to our own events processor
    client._to_file = types.MethodType(overwrite,
                                        client)
    client.start = types.MethodType(_start_overwrite, client)
    client.start()
