from flask_caching import Cache
import os

cache = Cache(config={'CACHE_TYPE': 'RedisCache', 'CACHE_REDIS_URL': os.environ.get('REDIS_URL')})
