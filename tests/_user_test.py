import json

import pytest
import requests
from app import app, db
from database.models.User import User

base_url = "http://127.0.0.1:5000/api"

userData = {"fullname": "test", "email": "test@email.com", "password": "123456"}

session = requests.Session()
session.headers.update([("Content-Type", "application/json")])

# remove test user
with app.app_context():
    obj = User.query.filter(User.email == userData["email"]).first()
    if obj:
        db.session.delete(obj)
        db.session.commit()


def test_create_user():
    """Create user"""
    url = base_url + "/users/"
    data = json.dumps(userData)
    res = session.post(url, data=data)
    assert res.status_code == 201


def test_user_login():
    """Login user"""
    url = base_url + "/auth/login"
    data = json.dumps({"email": userData["email"], "password": userData["password"]})
    res = session.post(url, data=data)
    assert res.status_code == 200
    token = res.json()["token"]
    session.headers.update([("Authorization", token)])


def test_user_info():
    """Fetch user info"""
    url = base_url + "/users/info"
    res = session.get(url)
    assert res.status_code == 200
    global user
    user = res.json()


@pytest.mark.skip
@pytest.mark.parametrize(
    "data",
    [
        {"fullname": "username2"},
        {"fullname": "username3", "password": "password2"},
    ],
)
def test_update_user_info(data):
    """Update user info"""
    url = base_url + "/users/" + str(user["id"])
    res = session.put(url, data=json.dumps(data))
    assert res.status_code == 200


def test_delete_user():
    """Delete user"""
    url = base_url + "/users/" + str(user["id"])
    res = session.delete(url)
    assert res.status_code == 204
