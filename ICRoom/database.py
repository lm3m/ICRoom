from redis import Redis, RedisError

# Connect to Redis
redis = Redis(host="redis", decode_responses=True, db=0, socket_connect_timeout=2, socket_timeout=2)

