import redis
from flask import Flask
from my_function.backend.services.redis_cache_service import RedisConnectionHandler, RedisCacheService
import os
from my_function.backend.services.pcf_service import register_routes

def create_app():
    global cache_service
    
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    
    redis_handler = RedisConnectionHandler(
        host=os.environ.get('REDIS_CACHE_HOST'),
        port=int(os.environ.get('REDIS_CACHE_PORT', 6380)),
        password=os.environ.get('REDIS_CACHE_PASSWORD',None),
    )
    cache_service = RedisCacheService(redis_handler)
    
    app = Flask(
        __name__,
        template_folder=os.path.join(BASE_DIR, 'frontend', 'templates'),
        static_folder=os.path.join(BASE_DIR, 'frontend', 'static')
    )
    
    register_routes(app,cache_service)
    
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)