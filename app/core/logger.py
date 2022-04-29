import logging

LOGGER_LEVEL = logging.INFO
LOGGER_NAME = 'API_LOGGER'

logging.basicConfig(
    # filename='api_log_file',
    filemode='a',
    format='[%(asctime)s] %(name)s - %(levelname)s: %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S',
    level=LOGGER_LEVEL
)

API_LOGGER = logging.getLogger(LOGGER_NAME)
API_LOGGER.setLevel(LOGGER_LEVEL)
