import logging
import os
import shutil
import signal
import subprocess
from copy import copy
import pytest
import requests
from utils.decorators import wait_server_up
from fixtures import *

repo_root = os.path.abspath(os.path.join(__file__, os.pardir))  # final project path


def start_mock():
    mock_path = os.path.join(repo_root, '../mock', 'vk_api', 'flask_mock.py')

    mock_out = open('/tmp/mock_stdout.log', 'w')
    mock_err = open('/tmp/mock_stderr.log', 'w')

    env = copy(os.environ)
    # env['APP_HOST'] = settings.APP_HOST
    # env['APP_PORT'] = settings.APP_PORT
    #
    # env['STUB_HOST'] = settings.STUB_HOST
    # env['STUB_PORT'] = settings.STUB_PORT
    # TODO: remove hardcoded values
    env['MOCK_HOST'] = '0.0.0.0'
    env['MOCK_PORT'] = '8088'

    proc = subprocess.Popen(['python3.8', mock_path], stdout=mock_out, stderr=mock_err, env=env)

    config.mock_proc = proc
    config.mock_out = mock_out
    config.mock_err = mock_err

    wait_server_up(requests.get, 5, url=f'http://{env["MOCK_HOST"]}:{env["MOCK_PORT"]}')


def stop_mock():
    config.mock_proc.send_signal(signal.SIGINT)
    exit_code = config.mock_proc.wait()

    config.mock_out.close()
    config.mock_err.close()

    # assert exit_code == 0


def pytest_addoption(parser):
    parser.addoption('--url', default='http://myapp:8090')
    parser.addoption('--browser', default='chrome')
    parser.addoption('--selenoid', action='store_true')
    parser.addoption('--debug_log', action='store_true')


@pytest.fixture(scope='session')
def config(request):
    url = request.config.getoption('--url')
    browser = request.config.getoption('--browser')
    if request.config.getoption('--selenoid'):
        # TODO: setup env variables in docker-compose
        # selenoid = f'http://{os.environ.get(SELENOID_HOST,"127.0.0.1")}:{os.environ.get(SELENOID_PORT,"4444")}'
        selenoid = f'http://127.0.0.1:4444'
    else:
        selenoid = None
    debug_log = request.config.getoption('--debug_log')
    # return {'url': url, 'browser': browser, 'debug_log': debug_log}
    return {'url': url, 'browser': browser, 'selenoid': selenoid, 'debug_log': debug_log}


def pytest_configure(config):
    base_test_dir = '/tmp/tests'
    if not hasattr(config, 'workerinput'):
        # start_mock()

        if os.path.exists(base_test_dir):
            shutil.rmtree(base_test_dir)
        os.makedirs(base_test_dir)

    config.base_test_dir = base_test_dir


def pytest_unconfigure(config):
    if not hasattr(config, 'workerinput'):
        # stop_mock()
        pass


@pytest.fixture(scope='function')
def test_dir(request):
    test_name = request._pyfuncitem.nodeid.replace('/', '_').replace(':', '_')
    test_dir = os.path.join(request.config.base_test_dir, test_name)
    os.makedirs(test_dir)
    return test_dir


@pytest.fixture(scope='function', autouse=True)
def logger(test_dir):
    log_formatter = logging.Formatter('%(asctime)s - %(filename)-15s - %(levelname)-6s - %(message)s')
    log_file = os.path.join(test_dir, 'test.log')

    log_level = logging.DEBUG

    file_handler = logging.FileHandler(log_file, 'w')
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(log_level)

    log = logging.getLogger('test')
    log.propagate = False
    log.setLevel(log_level)
    log.handlers.clear()
    log.addHandler(file_handler)

    yield log

    for handler in log.handlers:
        handler.close()
