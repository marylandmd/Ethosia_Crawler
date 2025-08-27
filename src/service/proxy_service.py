import itertools
import threading


class ProxyService:
    _proxies = None
    _instance = None
    _instance_lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super(ProxyService, cls).__new__(cls, *args, **kwargs)
                cls._proxies = ["113.172.249.184:21253"]
                cls._proxy_pool = itertools.cycle(cls._proxies)
        return cls._instance

    def get(self):
        next_value = next(self._proxy_pool)
        return {
            'http': f'http://{next_value}',
            'https': f'https://{next_value}'
        }
