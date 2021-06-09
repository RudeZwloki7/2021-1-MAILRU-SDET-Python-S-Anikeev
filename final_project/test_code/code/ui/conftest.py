import logging
import shutil
from orm.client import MysqlClient
from ui.fixtures import *

repo_root = os.path.abspath(os.path.join(__file__, os.pardir))  # final project path


def pytest_addoption(parser):
    parser.addoption('--url', default='http://myapp:8090')
    parser.addoption('--browser', default='chrome')
    parser.addoption('--selenoid', action='store_true')
    parser.addoption('--debug_log', action='store_true')


@pytest.fixture(scope='session')
def config(request):
    url = request.config.getoption('--url')
    browser = request.config.getoption('--browser')
    # if request.config.getoption('--selenoid'):
    selenoid = f'http://selenoid:4444'
    # else:
    #     selenoid = None
    debug_log = request.config.getoption('--debug_log')
    return {'url': url, 'browser': browser, 'selenoid': selenoid, 'debug_log': debug_log}


def pytest_configure(config):
    base_test_dir = '/tmp/tests'
    if not hasattr(config, 'workerinput'):

        if os.path.exists(base_test_dir):
            shutil.rmtree(base_test_dir)
        os.makedirs(base_test_dir)

    config.base_test_dir = base_test_dir


# def pytest_unconfigure(config):
#     if not hasattr(config, 'workerinput'):
#         # stop_mock()
#         pass


@pytest.fixture(scope='function')
def test_dir(request):
    test_name = request._pyfuncitem.nodeid.replace('/', '_').replace(':', '_')
    test_dir = os.path.join(request.config.base_test_dir, test_name)
    os.makedirs(test_dir)
    return test_dir


@pytest.fixture(scope='session')
def mysql_client():
    mysql_client = MysqlClient(user='test_qa', password='qa_test', db_name='test_db')
    mysql_client.connect()
    yield mysql_client
    mysql_client.connection.close()


@pytest.fixture(scope='function', autouse=True)
def logger(test_dir, config):
    log_formatter = logging.Formatter('%(asctime)s - %(filename)-15s - %(levelname)-6s - %(message)s')
    log_file = os.path.join(test_dir, 'test.log')

    log_level = logging.DEBUG if config['debug_log'] else logging.INFO

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

    with open(log_file, 'r') as f:
        allure.attach(f.read(), 'test.log', attachment_type=allure.attachment_type.TEXT)
