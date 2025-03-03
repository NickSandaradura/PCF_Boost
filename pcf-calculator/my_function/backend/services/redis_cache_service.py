from redis import Redis, ConnectionPool, ConnectionError, TimeoutError
from redis.retry import Retry
from redis.backoff import ExponentialBackoff
import time
from functools import wraps

class RedisConnectionHandler:
    def __init__(self, host, port, password=None,ssl=True, retry_count=3):
        self.connection_settings = {
            'host': host,
            'port': port,
            'password': password,
            # 'ssl':ssl,
            # 'ssl_cert_reqs': None,
            'socket_timeout': 5,  
            'socket_connect_timeout': 5,  
            'socket_keepalive': True,  
            'health_check_interval': 30,  
            'retry': Retry(  
                ExponentialBackoff(),
                retry_count
            )
        }
        
        self.pool = None
        self.client = None
        self.initialize_connection()

    def initialize_connection(self):
        try:
            self.pool = ConnectionPool(**self.connection_settings)
            self.client = Redis(connection_pool=self.pool)

            self.client.ping()
        except (ConnectionError, TimeoutError) as e:
            print(f"Initial connection failed: {str(e)}")
            raise

    def reconnect(self):
        try:
            if self.pool:
                self.pool.disconnect()
            self.initialize_connection()
            return True
        except (ConnectionError, TimeoutError):
            return False

def with_redis_retry(max_retries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(self, *args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    retries += 1
                    if retries == max_retries:
                        raise e
                    print(f"Redis operation failed, attempt {retries} of {max_retries}")
                    if self.reconnect():
                        time.sleep(delay)
                    else:
                        time.sleep(delay * 2)
            return None
        return wrapper
    return decorator

class RedisCacheService:
    def __init__(self, redis_handler):
        self.redis = redis_handler

    @with_redis_retry(max_retries=3)
    def setex(self, key, ttl, value):
        """Setzt einen Wert mit Ablaufzeit"""
        return self.redis.client.setex(key, ttl, value)

    @with_redis_retry(max_retries=3)
    def get(self, key):
        """Holt einen Wert"""
        return self.redis.client.get(key)