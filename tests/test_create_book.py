from app import app
from database_connection import DatabaseConnection
from playwright.sync_api import Page, expect

def test_cant_create_book_when_unauthed(page: Page):
    connection = DatabaseConnection()
    connection.connect()
    connection.execute("TRUNCATE TABLE users;")
    
    page.goto("http://127.0.0.1:5001/add_book")
    
    page.get_by_placeholder("Title").fill("OK Book")
    page.get_by_placeholder("Author").fill("Fine Author")
    page.get_by_role("button", name="Submit").click()

    assert page.url == "http://127.0.0.1:5001/sessions/new"

    page.goto("http://127.0.0.1:5001/books")
    titles = page.locator('.book_item h2')

    assert titles.all_inner_texts()[-1] != "OK Book"


def test_form_submits_a_book(page: Page):
    connection = DatabaseConnection()
    connection.connect()
    connection.execute("TRUNCATE TABLE users;")
    connection.execute("INSERT INTO users (username, password) values ('testuser', 'password123');")

    page.goto("http://127.0.0.1:5001/sessions/new")

    page.get_by_placeholder("Insert username here").fill("testuser")
    page.get_by_placeholder("Insert password here").fill("password123")
    page.get_by_role("button", name="Log in").click()

    page.goto("http://127.0.0.1:5001/add_book")

    page.get_by_placeholder("Title").fill("OK Book")
    page.get_by_placeholder("Author").fill("Fine Author")
    page.get_by_role("button", name="Submit").click()

    page.goto("http://127.0.0.1:5001/books")

    titles = page.locator('.book_item h2')
    new_title = titles.all_inner_texts()[-1]
    authors = page.locator('.book_item p')
    new_author = authors.all_inner_texts()[-1]

    assert new_title == "OK Book"
    assert new_author == "Fine Author"

def test_create_book_is_saved_to_database():
    client = app.test_client()

    connection = DatabaseConnection()
    connection.connect()
    connection.seed('seeds/book_store.sql')    
    connection.seed('seeds/users.sql')

    response_users = client.post('/users/new', data={
        'username': 'testuser2',
        'password': 'password123'
    })

    response_sessions = client.post('/sessions/new', data={
        'username': 'testuser2',
        'password': 'password123'
    })

    response_books = client.post('/add_book', data={
        'title': 'test_book',
        'author': 'test_author'
    })

    assert response_books.status_code == 302

    result = connection.execute("SELECT * FROM books WHERE title = 'test_book' and author = 'test_author'")

    assert len(result) == 1
    assert result[0]['title'] == 'test_book'