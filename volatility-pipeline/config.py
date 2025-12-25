# config.py
import os

# We get the path of the folder where this file sits
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# We name the database file 'quant.db'
DB_NAME = os.path.join(BASE_DIR, 'quant.db')
TARGET_TICKER = "AMD"