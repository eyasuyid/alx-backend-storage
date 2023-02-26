#!/usr/bin/env python3
"""Writing strings to Redis"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """count calls"""
    method_key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwds):
        self._redis.incr(method_key)
        return method(self, *args, **kwds)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Stores the history of inputs and outputs for a particular function"""
    method_key = method.__qualname__
    inputs, outputs = method_key + ':inputs', method_key + ':outputs'

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.rpush(inputs, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(result))
        return result
    return wrapper


def replay(method: Callable) -> None:
    """Displays the history of calls of a particular function"""
    method_key = method.__qualname__
    inputs, outputs = method_key + ':inputs', method_key + ':outputs'
    redis = method.__self__._redis
    method_count = redis.get(method_key).decode('utf-8')
    print(f'{method_key} was called {method_count} times:')
    IOTuple = zip(redis.lrange(inputs, 0, -1), redis.lrange(outputs, 0, -1))
    for inp, outp in list(IOTuple):
        attr, data = inp.decode("utf-8"), outp.decode("utf-8")
        print(f'{method_key}(*{attr}) -> {data}')


class Cache:
    """Cache class"""
    def __init__(self):
        """Instanciation"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Return uuid"""
        myuuid = str(uuid.uuid4())
        self._redis.set(myuuid, data)
        return myuuid

    def get(self, key: str, fn: Optional[Callable] = None) -> str:
        """used to convert the data back to the desired format."""
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data

    def get_str(self, data: str) -> str:
        """get str"""
        return data.decode('utf-8', 'strict')

    def get_int(self, data: str) -> int:
        """get int"""
        return int(data)
