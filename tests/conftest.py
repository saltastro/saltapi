import pytest

from run import get_app


@pytest.fixture
def app():
    app = get_app()
    return app


@pytest.fixture
def client(app):
    return app.test_client()
