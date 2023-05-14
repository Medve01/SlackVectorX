from pickledb import PickleDB
from config import Config

config = Config()

db = PickleDB(config.get("DATA_DIR") + '/' + config.get("DATABASE"), auto_dump=True, sig=False)

def get(key):
    return db.get(key)

def set(key, value):
    db.set(key, value)

def delete(key):
    db.rem(key)
