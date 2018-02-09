import tinydb
from tinydb.storages import MemoryStorage
tiny_db = tinydb.TinyDB(storage=MemoryStorage)
