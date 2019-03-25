# encoding: utf-8
import subprocess
import os

ADMIN_NAME = subprocess.Popen('whoami', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf8').strip()

HOST = "127.0.0.1"
PORT = 27089
USER_DATA_DIR = os.path.dirname(os.path.abspath('manage.py')) + '/User_dir'
DATABASE_PATH = os.path.dirname(os.path.abspath('manage.py')) + '/db/user.ini'
BUFFER = 1024
