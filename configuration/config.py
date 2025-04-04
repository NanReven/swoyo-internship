import toml
from typing import Any
from logger.logger import get_logger

logger = get_logger()


def parse_config(config_path: str) -> dict[str, Any]:
    try: 
        config = toml.load(config_path)
    except TypeError:
        logger.error("config_path must be str")
        raise
    except toml.TomlDecodeError as e:
        logger.error(f"Error while decoding config.toml: {e}")
        raise
    return config


def validate_config(config: dict[str, Any]):
    for setting in ["request_settings", "user_settings"]:
        if setting not in config.keys():
            logger.error(f"Missing required setting in config.toml: {setting}")
            raise ValueError(f"Missing required setting in config.toml: {setting}")
    
    for user_setting in ["username", "password", "host"]:
        if user_setting not in config["user_settings"].keys():
            logger.error(f"Missing required user_setting in config.toml: {user_setting}")
            raise ValueError(f"Missing required user_setting in config.toml: {user_setting}")
        elif not isinstance(config["user_settings"][user_setting], str):
            logger.error(f"{user_setting} must be str")
            raise ValueError(f"{user_setting} must be str")
    
    for request_setting in ["port", "url", "host"]:
        if request_setting not in config["request_settings"]:
            logger.error(f"Missing required request_setting in config.toml: {request_setting}")
            raise ValueError(f"Missing required request_setting in config.toml: {request_setting}")
        elif request_setting != "port" and not isinstance(config["request_settings"][request_setting], str):
            logger.error(f"{request_setting} must be str")
            raise ValueError(f"{request_setting} must be str")
        elif request_setting == "port" and not isinstance(config["request_settings"][request_setting], int):
            logger.error(f"{request_setting} must be int")
            raise ValueError(f"{request_setting} must be int")
    
    if not (1024 <= config["request_settings"]["port"] <= 65535):
        logger.error(f"Port must be between 1024 and 65535")
        raise ValueError("Port must be between 1024 and 65535")

