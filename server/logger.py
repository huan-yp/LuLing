import logging

from logging import INFO, ERROR

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logger = logging.Logger("PythonServerLogger")
std_handler = logging.StreamHandler()
std_handler.setFormatter(logging.Formatter(LOG_FORMAT))
file_handler = logging.FileHandler("PythonServerLog.txt")
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
logger.addHandler(file_handler)
logger.addHandler(std_handler)