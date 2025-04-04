import json
import base64
import asyncio
from logger.logger import get_logger

logger = get_logger()


class HTTPRequest:
    def __init__(self, url: str, host: str, username: str, password: str, body_data: dict):
        self.url = url
        self.host = host
        self.username = username
        self.password = password
        self.body = json.dumps(body_data)

    def __str__(self):
        return (
            f"POST {self.url} HTTP/1.1\r\n"
            f"Host: {self.host}\r\n"
            f"Authorization: Basic {self.encode_credentials()}\r\n"
            "Content-Type: application/json\r\n"
            f"Content-Length: {len(self.body)}\r\n"
            "\r\n"
            f"{self.body}"
        )

    def encode_credentials(self) -> str:
        credentials = f"{self.username}:{self.password}"
        return base64.b64encode(credentials.encode()).decode()

    def to_bytes(self) -> bytes:
        request = (
            f"POST {self.url} HTTP/1.1\r\n"
            f"Host: {self.host}\r\n"
            f"Authorization: Basic {self.encode_credentials()}\r\n"
            "Content-Type: application/json\r\n"
            f"Content-Length: {len(self.body)}\r\n"
            "\r\n"
            f"{self.body}"
        )
        return request.encode()


class HTTPResponse:
    def __init__(self, response_code: str, response_body: str):
        self.status_code = response_code
        self.response_body = response_body

    @staticmethod
    def from_bytes(binary_data: bytes):
        try:
            headers, body = binary_data.split(b"\r\n\r\n")
            status_line = headers.split(b"\r\n")[0]
            status_code = status_line.split(b" ")[1].decode()
            return HTTPResponse(response_code=status_code, response_body=body.decode())
        except Exception as e:
            logger.error(f"Error parsing HTTP response: {e}")
            raise ValueError(f"Error parsing http response: {e}")

    def __str__(self):
        return f"Response code: {self.status_code}\nResponse body: {self.response_body}"


async def send_request(config, args):
    try:
        request = HTTPRequest(
            url=config["request_settings"]["url"],
            host=config["request_settings"]["host"],
            username=config["user_settings"]["username"],
            password=config["user_settings"]["password"],
            body_data={
                "sender": args.sender,
                "recipient": args.recipient,
                "message": args.message,
            }
        )

        reader, writer = await asyncio.open_connection(
            config["request_settings"]["host"],
            config["request_settings"]["port"]
        )

        writer.write(request.to_bytes())
        await writer.drain()
        logger.info(f"Request sent to server: {request}")

        data = await reader.read(1024)
        if not data:
            logger.info("Connection was closed by server")
            return

        response = HTTPResponse.from_bytes(data)
        print(response)
        logger.info(f"Server response: {response}")

        writer.close()
        await writer.wait_closed()
        logger.info("Connection closed")

    except OSError as e:
        logger.error(f"Network error: {e}")
        raise
    except ValueError as e:
        logger.error(f"Validation or parsing error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise
