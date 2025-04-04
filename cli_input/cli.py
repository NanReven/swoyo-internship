import argparse
from logger.logger import get_logger

logger = get_logger()


def parse_cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CLI for send sms")
    parser.add_argument(
        "--sender",
        type=str,
        help="Sender number",
        required=True
    )
    parser.add_argument(
        "--recipient",
        type=str,
        help="Recipient number",
        required=True
    )
    parser.add_argument(
        "--message",
        type=str,
        help="Message to send",
        required=True
    )
    args = parser.parse_args()
    logger.info(f"Parsed CLI args: sender={args.sender}, recipient={args.recipient}, message={args.message}")
    return args


def validate_cli_args(sender: str, recipient: str):
    if not (sender.isdigit() and recipient.isdigit()):
        logger.error("Sender's number and recipient's number must contain only digits")
        raise ValueError("Sender's number and recipient's number must contain only digits")
    elif len(sender) != 11 or len(recipient) != 11:
        logger.error("Wrong phone number format")
        raise ValueError("Wrong phone number format")
    elif sender == recipient:
        logger.error("Sender's number must be different from recipient's number")
        raise ValueError("Sender's number must be different from recipient's number")
