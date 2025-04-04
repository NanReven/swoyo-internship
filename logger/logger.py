import logging


def get_logger() -> logging.Logger:
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG) 

    if not logger.handlers:
        file_handler = logging.FileHandler("app.log")
        file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        stream_handler.setFormatter(stream_formatter)
        stream_handler.setLevel(logging.ERROR)
        logger.addHandler(stream_handler)

    return logger
