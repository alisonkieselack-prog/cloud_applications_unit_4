from playwright.sync_api import Page, expect
from book_repository import *
from database_connection import *

def test_has_title(page: Page):
    page.goto("http://127.0.0.1:5001/books")

    header = page.locator("header")

    expect(header).to_have_text("My favourite books")

def test_book_list_contains_all_books(page: Page):
    connection = DatabaseConnection()
    connection.connect()
    connection.seed("./seeds/book_store.sql")

    page.goto("http://127.0.0.1:5001/books")

    titles = page.locator('.book_item h2')
    authors = page.locator('.book_item p')

    expected_titles = [
        'The Gruffalo',
        'Ada Twist, Scientist',
        'The Girl Who Drank the Moon',
        'Dragons in a Bag'
        ]
    expected_authors = [
        'Julia Donaldson',
        'Andrea Beaty',
        'Kelly Barnhill',
        'Zetta Elliott'
        ]

    actual_titles = titles.all_inner_texts()
    actual_authors = authors.all_inner_texts()

    assert actual_titles == expected_titles
    assert actual_authors == expected_authors

def test_form_submits_a_book(page: Page):
    connection = DatabaseConnection()
    connection.connect()
    connection.seed("./seeds/book_store.sql")

    page.goto("http://127.0.0.1:5001/books")

    page.get_by_placeholder("Title").fill("OK Book")
    page.get_by_placeholder("Author").fill("Fine Author")
    page.get_by_role("button", name="Submit").click()

    titles = page.locator('.book_item h2')
    new_title = titles.all_inner_texts()[-1]
    authors = page.locator('.book_item p')
    new_author = authors.all_inner_texts()[-1]

    assert new_title == "OK Book"
    assert new_author == "Fine Author"