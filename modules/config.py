import configparser
from typing import cast

from modules import datatype
from modules._except import InitError


def get_config() -> datatype.Config:
    config = configparser.ConfigParser()

    file = config.read("user.cfg")
    if not file:
        raise InitError.ConfigNotFoundError

    detail = config["Config"]
    return cast(datatype.Config, dict(detail))

def replace_config_values(config: datatype.Config, home_path: str):
    for setting, value in config.items():
        value = cast(str, value)
        if "!Home" in value:
            replaced_value = value.replace("!Home", home_path)
            config[setting] = replaced_value

"""
    if config["max_concurrent_thread_number"]:
        threads = system.get_threads()
        if threads is None:
            console.write("논리 쓰레드 갯수를 알 수 없습니다.\n" \
            "1로 사용합니다.", Color.RED)
            threads = 0
        config["max_concurrent_thread_number"] = (threads * 2) + 1
"""
