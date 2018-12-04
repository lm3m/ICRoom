from fakeredis import FakeStrictRedis

fixed_fake_redis = FakeStrictRedis(decode_responses=True)

# mocking zadd for fake redis, redispy 3 changes the zadd 
# takes a dict now, not a series of pairs
_zadd = fixed_fake_redis.zadd

def unpack_zadddef(name, mapping):
     for key, value in mapping.items():
         return _zadd(name, value, key)

fixed_fake_redis.zadd = unpack_zadddef

