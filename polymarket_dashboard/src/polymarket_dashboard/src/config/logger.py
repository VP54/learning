import logging

log_formatter = logging.Formatter(fmt="%(asctime)s | [%(threadName)-12.12s] | %(levelname)s | %(message)s")

logger = logging.getLogger()
fileHandler = logging.FileHandler("./polymarket_dashboard.log", mode='a')
fileHandler.setFormatter(log_formatter)
logger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(log_formatter)
logger.addHandler(consoleHandler)


def create_logger(level=logging.INFO, name="db"):
    log_formatter = logging.Formatter(
        fmt="%(asctime)s | [%(threadName)-12.12s] | %(levelname)s | %(message)s"
    )

    logger = logging.getLogger()
    fileHandler = logging.FileHandler("./polymarket_dashboard.log", mode="a")
    fileHandler.setFormatter(log_formatter)
    logger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(log_formatter)
    logger.addHandler(consoleHandler)
    return logger