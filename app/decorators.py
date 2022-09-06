from pymongo import MongoClient
import functools
import secret

def client_open(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        client = MongoClient(f'mongodb://{secret.LOGIN}:{secret.PASSWD}@localhost:27017')
        func(*args, **kwargs, **client)
        client.close()
    return wrapper