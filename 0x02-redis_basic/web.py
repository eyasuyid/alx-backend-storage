#!/usr/bin/env python3
<<<<<<< HEAD
"""
Implements an expiring web cache and tracker
"""
from typing import Callable
from functools import wraps
import redis
import requests
redis_client = redis.Redis()
=======
""" Redis Module """

from functools import wraps
import redis
import requests
from typing import Callable
>>>>>>> e4a56d389cc93e42547b2bd2b456b2996cf6b4c8

redis_ = redis.Redis()

<<<<<<< HEAD
def url_count(method: Callable) -> Callable:
    """counts how many times an url is accessed"""
    @wraps(method)
    def wrapper(*args, **kwargs):
        url = args[0]
        redis_client.incr(f"count:{url}")
        cached = redis_client.get(f'{url}')
        if cached:
            return cached.decode('utf-8')
        redis_client.setex(f'{url}, 10, {method(url)}')
        return method(*args, **kwargs)
    return wrapper


@url_count
def get_page(url: str) -> str:
    """get a page and cache value"""
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
=======

def count_requests(method: Callable) -> Callable:
    """ Decortator for counting """
    @wraps(method)
    def wrapper(url):  # sourcery skip: use-named-expression
        """ Wrapper for decorator """
        redis_.incr(f"count:{url}")
        cached_html = redis_.get(f"cached:{url}")
        if cached_html:
            return cached_html.decode('utf-8')
        html = method(url)
        redis_.setex(f"cached:{url}", 10, html)
        return html

    return wrapper


@count_requests
def get_page(url: str) -> str:
    """ Obtain the HTML content of a  URL """
    req = requests.get(url)
    return req.text
>>>>>>> e4a56d389cc93e42547b2bd2b456b2996cf6b4c8
