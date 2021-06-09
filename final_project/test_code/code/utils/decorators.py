import time
from requests.exceptions import ConnectionError


def wait_server_up(method, timeout=5, **kwargs):
    started = False
    st = time.time()
    while time.time() - st <= timeout:
        try:
            method(**kwargs)
            started = True
            break
        except ConnectionError:
            pass

    if not started:
        raise RuntimeError(f'Server did not started in {timeout}s!')
