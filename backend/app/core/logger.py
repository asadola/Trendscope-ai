from loguru import logger
import sys


def setup_logger(log_level: str):
    logger.remove()
    logger.add(
        sys.stdout,
        level=log_level,
        format="<green>{time}</green> | <level>{level}</level> | <cyan>{message}</cyan>",
    )
    return logger
