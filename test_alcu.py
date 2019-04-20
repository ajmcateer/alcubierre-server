import os
import tempfile

import pytest
from . import app, database
from .shared import db


@pytest.fixture
def client():
    db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
    app.app.config['TESTING'] = True
    client = app.app.test_client()

    with app.app.app_context():
        database.init_db()

    yield client

    os.close(db_fd)
    os.unlink(app.app.config['DATABASE'])


def test_landing_page(client):
    """Start with a blank database."""

    rv = client.get('/')
    print(rv.data)
    assert b"I'm Alive" in rv.data


def test_create_channel():
    rv = create_channel(client)
    assert b'You were logged in' in rv.data


def create_channel(client):
    return client.post('create', data=dict(
        username="Test1"
    ))
