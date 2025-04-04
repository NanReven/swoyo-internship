import asyncio
from configuration.config import parse_config, validate_config
from cli_input.cli import parse_cli_args, validate_cli_args
from http.send_request import send_request
from logger.logger import get_logger


if __name__ == "__main__":
    logger = get_logger()
    try:
        config = parse_config("./configuration/config.toml")
        validate_config(config)
        args = parse_cli_args()
        validate_cli_args(args.sender, args.recipient)
        asyncio.run(send_request(config, args))
    except Exception as e:
        logger.error(f"Error: {e}")

