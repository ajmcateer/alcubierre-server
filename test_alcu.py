import os
import tempfile
import datetime
import pytest
from . import app, database
from .shared import db
from random import randint
import json
import uuid


@pytest.fixture
def client():
    app.app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
    app.app.config['TESTING'] = True
    client = app.app.test_client()

    with app.app.app_context():
        database.init_db()

    yield client


def test_landing_page(client):
    rv = client.get('/')
    assert b"I'm Alive" in rv.data


def test_create_channel_without_name(client):
    rv = client.post('/channels/create', data=dict())
    assert b'"Error":"name is required"' in rv.data


def test_create_channel_with_name(client):
    #time = round(datetime.datetime.now().timestamp())
    rand = randint(1000000, 9999999)
    rv = client.post('/channels/create', data=dict(
        name=rand))
    assert b'"created":' in rv.data


def test_get_channel(client):
    time = round(datetime.datetime.now().timestamp() + 1)
    rand = randint(1000000, 9999999)
    response_one = client.post('/channels/create', data=dict(
        name=rand))
    assert b'"created":' in response_one.data

    response_two = client.get('/channels?name={}'.format(rand))
    print(response_two.data)
    assert b"created" in response_two.data


def test_get_fake_channel(client):
    rand = randint(1000000, 9999999)

    response_two = client.get('/channels?name={}'.format(rand))
    print(response_two.data)
    assert b'"Error":"Channel' in response_two.data


def test_duplicate_channel(client):
    rand = randint(1000000, 9999999)
    response_one = client.post('/channels/create', data=dict(
        name=rand))
    assert b'"created":' in response_one.data

    response_two = client.post('/channels/create', data=dict(
        name=rand))
    assert b'"Error":"name' in response_two.data


# def test_delete_channel(client):
#     rand = randint(1000000, 9999999)
#     response_one = client.post('/channels/create', data=dict(
#         name=rand))
#     resp = json.loads(response_one.data.decode('utf8').replace("'", '"'))
#
#     di = {"name": rand, "admin_key": resp["admin_key"]}
#     response_two = client.post('/channels/delete', data=di)
#     assert b'"Error":"name' in response_two.data


def test_register_device(client):
    response_one = client.post('/devices/register', data=dict(
        name="test_device_1", uuid=uuid.uuid4(), message_type="http"))
    assert b'"created":' in response_one.data


def test_register_device_without_name(client):
    response_one = client.post('/devices/register', data=dict(
         uuid=uuid.uuid4(), message_type="http"))
    assert b'name is required' in response_one.data


def test_register_device_without_uuid(client):
    response_one = client.post('/devices/register', data=dict(
          name="test_device_1", message_type="http"))
    assert b'uuid is required' in response_one.data


def test_register_device_without_message_type(client):
    response_one = client.post('/devices/register', data=dict(
        name="test_device_1", uuid=uuid.uuid4()))
    assert b'message_type is required' in response_one.data


def test_register_device_duplicate(client):
    new_uuid=uuid.uuid4()
    response_one = client.post('/devices/register', data=dict(
        name="test_device_1", uuid=new_uuid, message_type="http"))

    response_two = client.post('/devices/register', data=dict(
        name="test_device_1", uuid=new_uuid, message_type="http"))
    assert b'is already registered' in response_two.data


def test_subscribe(client):
    device = uuid.uuid4()
    response_one = client.post('/devices/register', data=dict(
        name="test_device_1", uuid=device, message_type="http"))

    rand = randint(1000000, 9999999)
    response_two = client.post('/channels/create', data=dict(
        name=rand))
    print("TEST:" + str(response_two.json))
    data = json.loads(response_two.data)
    listen_key = data["listen_key"]

    response_three = client.post('/subscription/subscribe', data=dict(
        uuid=device, channel_key=listen_key))
    assert b'"channel_key":"' in response_three.data


def test_subscribe_without_uuid(client):
    device = uuid.uuid4()
    response_one = client.post('/devices/register', data=dict(
        name="test_device_1", uuid=device, message_type="http"))

    rand = randint(1000000, 9999999)
    response_two = client.post('/channels/create', data=dict(
        name=rand))
    print("TEST:" + str(response_two.json))
    data = json.loads(response_two.data)
    listen_key = data["listen_key"]

    response_three = client.post('/subscription/subscribe', data=dict(
        channel_key=listen_key))
    assert b'"Error":"uuid is required"' in response_three.data


def test_subscribe_without_channel_key(client):
    device = uuid.uuid4()
    response_one = client.post('/devices/register', data=dict(
        name="test_device_1", uuid=device, message_type="http"))

    rand = randint(1000000, 9999999)
    response_two = client.post('/channels/create', data=dict(
        name=rand))
    print("TEST:" + str(response_two.json))
    data = json.loads(response_two.data)
    listen_key = data["listen_key"]

    response_three = client.post('/subscription/subscribe', data=dict(
        uuid=device))
    assert b'"Error":"channel_key is required"' in response_three.data


def test_subscribe_with_bad_uuid(client):
    device = uuid.uuid4()

    rand = randint(1000000, 9999999)
    response_two = client.post('/channels/create', data=dict(
        name=rand))
    print("TEST:" + str(response_two.json))
    data = json.loads(response_two.data)
    listen_key = data["listen_key"]

    response_three = client.post('/subscription/subscribe', data=dict(
        uuid=device))
    assert b'5' in response_three.data