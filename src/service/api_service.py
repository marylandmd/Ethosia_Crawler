import requests


def session_pool(num_sessions):
    return [requests.Session() for _ in range(num_sessions)]
