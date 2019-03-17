# encoding: utf-8

import logging

test_log = logging.getLogger('test')
test_log.setLevel(logging.INFO)
stream_handler = logging.StreamHandler()
formater = logging.Formatter("%(asctime)s %(message)s",datefmt='%m/%d/%Y %I:%M:%S %p')
stream_handler.setFormatter(formater)
test_log.addHandler(stream_handler)

