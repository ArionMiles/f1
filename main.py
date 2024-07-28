import json
import logging
import os

from f1.live_data import runner
from f1.bulb_controller import get_devices

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
log_level = os.environ.get("LOG_LEVEL", "INFO")
logger.setLevel(log_level)

def get_drivers(filepath: str):
    with open(filepath) as f:
        return json.load(f)

if __name__ == '__main__':
    logger.info("Starting up...")
    logger.info("Loading devices info...")
    devices = get_devices("data/devices.json")

    logger.info("Loading drivers info...")
    drivers = get_drivers("data/drivers.json")

    runner(devices, drivers)