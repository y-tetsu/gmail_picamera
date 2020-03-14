#!/usr/bin/env python3
#==================
# parse command
#==================

import json
import re


def parse_command(setting, message):
    """
    parse command
    """
    execute_cmd = setting["execute"]
    pan_cmd = setting["pan"]
    tilt_cmd = setting["tilt"]

    execute = None
    try:
        execute = re.search(execute_cmd, message)
    except:
        pass

    ret = ""
    if execute:
        if re.search(pan_cmd, message):
            ret = "pan"
        if re.search(tilt_cmd, message):
            ret = "tilt"

    return ret


if __name__ == '__main__':
    import os

    setting = {
        "execute": "EXECUTE_COMMAND",
        "pan": "PAN_COMMAND",
        "tilt": "TILT_COMMAND"
    }

    setting_file = './setting.json'

    if os.path.isfile(setting_file):
        with open(setting_file) as f:
            setting = json.load(f)

    print(parse_command(setting, "カメラ"))
    print(parse_command(setting, "カメラパン"))
    print(parse_command(setting, "カメラチルト"))
