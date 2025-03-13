import redis
import json
import os
from dotenv import load_dotenv

load_dotenv()

redis_client = redis.Redis(
    host=os.getenv('REDIS_HOST'),
    port=int(os.getenv('REDIS_PORT')),
    decode_responses=True
)

def get_cache(key: str):
    cached = redis_client.get(key)
    return json.loads(cached) if cached else None

def set_cache(key: str, value, ttl=300):  # 5 minutes TTL
    redis_client.setex(key, ttl, json.dumps(value))