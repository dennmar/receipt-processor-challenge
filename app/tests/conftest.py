import pytest
from flask import Flask
from flask.testing import FlaskClient

from app import create_app

@pytest.fixture(scope='function')
def app() -> Flask:
    app = create_app()
    yield app

@pytest.fixture(scope='function')
def client(app: Flask) -> FlaskClient:
    return app.test_client()