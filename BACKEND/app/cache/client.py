import redis
import os
from dotenv import load_dotenv
from pathlib import Path


ENV_PATH = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path=ENV_PATH)
REDIS_HOST = os.getenv('REDIS_HOST')

# conection = redis.Redis(host=REDIS_HOST, port=6379, decode_responses=True)
connection = redis.asyncio.Redis(
    host=REDIS_HOST, port=6379, decode_responses=True
)
