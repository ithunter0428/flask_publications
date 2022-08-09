import json

import pytest
import requests
from app import app, db
from database.models.User import User
from database.models.Publication import Publication

base_url = "http://127.0.0.1:5000/api"

userData = {"fullname": "test", "email": "test@email.com", "password": "123456"}
publicationData = {"title": "Hello", "description": "World", "status": "request", "priority": "normal"}

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

def test_create_publication():
    """Create publication"""
    url = base_url + "/publications/"
    data = json.dumps(publicationData)
    res = session.post(url, data=data)
    assert res.status_code == 201

publications = None

def test_list_publication():
    """List publication"""
    url = base_url + "/publications/"
    res = session.get(url)
    assert res.status_code == 200
    global publications
    publications = res.json()


@pytest.mark.skip
@pytest.mark.parametrize(
    "data",
    [
        {"title": "No"},
        {"title": "Yes", "priority": "Critical"},
    ],
)
def test_update_publication_info(data):
    """Update publication info"""
    url = base_url + "/publications/" + str(publications[0]["id"])
    res = session.put(url, data=json.dumps(data))
    assert res.status_code == 200


def test_delete_publication():
    """Delete publication"""
    url = base_url + "/publications/" + str(publications[0]["id"])
    res = session.delete(url)
    assert res.status_code == 204
