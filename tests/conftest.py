import pytest
import os
from run import get_app

BASE_URL = 'http://localhost:5001'


@pytest.fixture(scope='session', autouse=True)
def set_base_uri():
    os.environ['SALT_API_BASE_URL'] = BASE_URL

    yield


@pytest.fixture()
def uri():
    def _make_uri(endpoint):
        return BASE_URL + endpoint

    yield _make_uri


@pytest.fixture
def app():
    app = get_app()
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def self(app):
    return self
