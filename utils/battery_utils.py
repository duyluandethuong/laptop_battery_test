import psutil
import time
import logging


def get_battery_level():
    logging.basicConfig(
        filename=f'logfilename.log',
        encoding='utf-8',
        level=logging.INFO,
        format='%(asctime)s | %(message)s'
    )

    battery = psutil.sensors_battery()
    plugged = battery.power_plugged
    percent = str(battery.percent)
    plugged = "Plugged In" if plugged else "Not Plugged In"

    log_string = f'Battery level: {percent}'
    print(log_string)

    logging.info(log_string)
    