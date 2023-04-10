from flaskr import create_app
import pytest


# See https://flask.palletsprojects.com/en/2.2.x/testing/
# for more info on testing
@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
    })
    return app

@pytest.fixture
def client(app):
    return app.test_client()

# TODO(Checkpoint (groups of 4 only) Requirement 4): Change test to
# match the changes made in the other Checkpoint Requirements.
def integration_home_page(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Welcome to our Wiki!" in resp.get_data()
    resp = client.get("/home")
    assert resp.status_code == 200
    assert b"Welcome to our Wiki!" in resp.get_data()


# TODO(Project 1): Write tests for other routes.
def integration_home_signup(client):
    resp = client.get("/signup")
    assert resp.status_code == 200
    assert b"Create an account" in resp.get_data()


def integration_home_login(client):
    resp = client.get("/login")
    assert resp.status_code == 200
    assert b"Log in" in resp.get_data()


def integration_upload(client):
    resp = client.get("/upload")
    assert resp.status_code == 200
    assert b"Select a file to upload:" in resp.get_data()


def integration_about(client):
    resp = client.get("/about")
    assert resp.status_code == 200
    assert b"Welcome to our Wiki!" in resp.get_data()


def integration_wiki_list(client):
    resp = client.get("/pages")
    assert resp.status_code == 200
    assert b"Pages contained in this Wiki" in resp.get_data()


def integration_wiki_page(client):
    resp = client.get("/pages/Super%20Mario%20Kart")
    assert resp.status_code == 200
    assert b"Super Mario Kart[a] is a kart racing game developed and published by Nintendo" in resp.get_data(
    )


# def integration_wiki_wikimusic_start(client):
#     resp = client.get("/wikimusic")
#     assert resp.status_code == 200
#     assert b"(Re)search for a song!" in resp.get_data()

# def test_wiki_wikimusic_post(client):
#     resp = client.post("/wikimusic")
#     assert resp.status_code == 200
#     assert b"(Re)search for a song!" in resp.get_data()

# def integration_wiki_wikimusic_notfound(client):
#     resp = client.get("/wikimusic")
#     assert resp.status_code == 200
#     assert b"(Re)search for a song!" in resp.get_data()

