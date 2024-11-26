# coding: utf-8
from pathlib import Path

# change DEBUG to False if you want to compile the code to exe
DEBUG = False


YEAR = 2023
AUTHOR = "Jumbla"
VERSION = "v0.0.1"
APP_NAME = "JumblaTools"

CONFIG_FOLDER = Path('AppData').absolute()
CONFIG_FILE = CONFIG_FOLDER / "config.json"
