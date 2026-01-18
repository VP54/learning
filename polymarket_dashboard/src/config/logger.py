import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s",)

logger = logging.getLogger("db")


def create_logger(level=logging.INFO, name="db"):
    logging.basicConfig(level=level, format="%(asctime)s | %(levelname)s | %(message)s",)

    logger = logging.getLogger(name)
    return logger