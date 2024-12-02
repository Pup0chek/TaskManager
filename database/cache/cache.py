import redis

def redis_client():
    return redis.StrictRedis(host="localhost", port="6379", db=0)


def main():
    r = redis_client()
    print(r.get('/').decode('utf-8'))


if __name__ == "__main__":
    main()