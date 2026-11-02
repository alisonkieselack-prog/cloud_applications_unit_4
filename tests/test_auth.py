from app import app
from database_connection import DatabaseConnection
from playwright.sync_api import Page

def test_auth_playwright(page: Page):

    connection = DatabaseConnection()
    connection.connect()
    connection.execute("TRUNCATE TABLE users;")
    connection.execute("INSERT INTO users (username, password) values ('test', '1234');")

    page.goto("http://localhost:5001/sessions/new")
    page.get_by_placeholder("username").fill("test")
    page.get_by_placeholder("password").fill("1234")
    page.get_by_role("button").click()

    assert page.url == "http://localhost:5001/books"

def test_auth_fails_playwright(page: Page):
    page.goto("http://localhost:5001/sessions/new")
    page.get_by_placeholder("username").fill("notauser")
    page.get_by_placeholder("password").fill("notapassword")
    page.get_by_role("button").click()

    assert page.url == "http://localhost:5001/sessions/new"

def test_auth_integration():
    client = app.test_client()
    connection = DatabaseConnection()
    connection.connect()
    connection.execute("TRUNCATE TABLE users;")
    connection.execute("INSERT INTO users (username, password) values ('test', '1234');")

    response = client.post('/sessions/new', data={
        'username': 'test',
        'password': '1234'
    })

    assert response.status_code == 302
    # this assertion might be new to you :)
    assert response.headers['Location'].endswith('/books')

def test_auth_fails_integration():
    client = app.test_client()
    connection = DatabaseConnection()
    connection.connect()
    connection.execute("TRUNCATE TABLE users;")

    response = client.post('/sessions/new', data={
        'username': 'notauser',
        'password': 'notapassword'
    })

    assert response.status_code == 302
    assert response.headers['Location'].endswith('/sessions/new')
