# lfu decorator
import functools
from collections import OrderedDict
import requests

def cache(max_limit=64):
    def internal(f):
        @functools.wraps(f)
        def deco(*args, **kwargs):
            cache_key = (args, tuple(kwargs.items()))

            if cache_key in deco._cache:
                deco._cache[cache_key][1] += 1
                return deco._cache[cache_key][0]

            else:
                result = f(*args, **kwargs)
                min_to_del = 0
                min_freq = float['inf']

                if len(deco._cache) >= max_limit:
                    min_to_del = None
                    min_freq = float['inf']

                    for key in deco._cache:
                        if deco._cache[key][1] < min_freq:
                            min_freq = deco._cache[key][1]
                            min_to_del = deco._cache[key][1]

                    if min_to_del is not None:
                        deco._cache.pop[min_to_del]

                deco._cache[cache_key] = [result, 1]
                return result

        deco._cache = OrderedDict()
        return deco

    return internal


def fetch_url(url, first_n=100):
    """Fetch a given url"""
    res = requests.get(url)
    return res.content[:first_n] if first_n else res.content


# Memory usage decorator
import tracemalloc


def memory_usage(f):
    @functools.wraps(f)
    def deco(*args, **kwargs):
        tracemalloc.start()
        start_snapshot = tracemalloc.take_snapshot()
        result = f(*args, **kwargs)
        end_snapshot = tracemalloc.take_snapshot()
        tracemalloc.stop()

        stats = end_snapshot.compare_to(start_snapshot, 'lineno')
        print(f"Використання пам'яті для функції {f.__name__}:")
        for stat in stats[:10]:
            print(stat)

        return result

    return deco


@memory_usage
def xx(a, b):
    return a + b


xx(2, 6)