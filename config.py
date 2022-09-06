import os
from decouple import config

class Config(object):
    try: # Dockerfile case
        CACHE_TYPE = os.environ['CACHE_TYPE']
        CACHE_REDIS_HOST = os.environ['CACHE_REDIS_HOST']
        CACHE_REDIS_PORT = os.environ['CACHE_REDIS_PORT']
        CACHE_REDIS_DB = os.environ['CACHE_REDIS_DB']
        CACHE_REDIS_URL = os.environ['CACHE_REDIS_URL']
        CACHE_DEFAULT_TIMEOUT = os.environ['CACHE_DEFAULT_TIMEOUT']
    except: # Virutalenv case
        CACHE_TYPE = config('CACHE_TYPE')
        CACHE_REDIS_HOST = config('CACHE_REDIS_HOST')
        CACHE_REDIS_PORT = config('CACHE_REDIS_PORT')
        CACHE_REDIS_DB = config('CACHE_REDIS_DB')
        CACHE_REDIS_URL = config('CACHE_REDIS_URL')
        CACHE_DEFAULT_TIMEOUT = config('CACHE_DEFAULT_TIMEOUT')

