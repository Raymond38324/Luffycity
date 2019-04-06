# coding: utf-8

import logging

logger = logging.getLogger('FtpServer')
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler('log/server.log')

file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s',datefmt='%m/%d/%Y %I:%M:%S %p')
stream_formatter = logging.Formatter('%(levelname)s - %(message)s')

stream_handler.setFormatter(stream_formatter)
file_handler.setFormatter(file_formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

