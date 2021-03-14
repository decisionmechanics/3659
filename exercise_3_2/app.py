import time
import redis
from flask import Flask

app = Flask(__name__)


def get_hit_count():
  cache = redis.Redis(host='redis', port=6379)

  # Increment the hit count, but allow for timeouts, e.g., on startup (using 5 retries and a timeout)

  retries = 5

  while True:
    try:
      return cache.incr('hits')
    except redis.exceptions.ConnectionError as exc:
      if retries == 0:
        raise exc

      retries -= 1

      time.sleep(0.5)


@app.route('/')
def hello():
  count = get_hit_count()

  return 'Hello from Docker! I have been seen {} times. \n'.format(count)