import os
import pytest


@pytest.fixture(scope='function')
def logo_path(repo_root):
    return os.path.join(repo_root, 'ui', 'logo.png')


@pytest.fixture(scope="function")
def generate_name():
    import random
    import string
    return ''.join(random.choices(string.ascii_letters + string.digits, k=7))
