import pytest

from http_socket.client import HttpClient
from utils.builder import Builder


class TestBase:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self):
        self.client: HttpClient = HttpClient()
        self.builder: Builder = Builder()
