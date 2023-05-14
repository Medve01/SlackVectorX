
from config import Config

config = Config()
if config.get("DATA_BACKEND") == "pickledb":
    import backends.pickledb as backend


def get(key):
    return backend.get(key)

def set(key, value):
    backend.set(key, value)

def delete(key):
    backend.delete(key)
