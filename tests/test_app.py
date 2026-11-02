import sys
import os

# this line is a bit of a hack which allows us to import app without changing anything else
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app

# a descriptive test name
def test_get_books_returns_a_200():
    # here's where we make the test client
    client = app.test_client()

    # here's where we make the request
    response = client.get("/books")

    # here's where we assert that the response's status code is 200
    assert response.status_code == 200

def test_get_authors_returns_200():
    client = app.test_client()
    response = client.get("/authors")

    assert response.status_code == 200

def test_get_authors_returns_list_of_authors():
    client = app.test_client()
    response = client.get("/authors")

    assert response.json == [
                {
                    "name": "Julia Donaldson",
                    "dob": "1948-09-16"
                },
                {
                    "name": "Andrea Beaty",
                    "dob": "1961-10-08"
                },
                {
                    "name": "Kelly Barnhill",
                    "dob": "1973-01-01"
                },
                {
                    "name": "Zetta Elliott",
                    "dob": "1979-11-11"
                }
                ]

def test_get_quote_returns_200():
    client = app.test_client()
    response = client.get("/quotes")

    assert response.status_code == 200
    
def test_get_quote_returns_quotes():
    client = app.test_client()
    response = client.get("/quotes")
    assert response.json == [
                {
                    "name": "George Eliot",
                    "quote": "It is never too late to be what you might have been."
                },
                {
                    "name": "C. S. Lewis",
                    "quote": "You are never too old to set another goal or to dream a new dream."
                },
                {
                    "name": "Maya Angelou",
                    "quote": "Nothing will work unless you do."
                },
                {
                    "name": "Eleanor Roosevelt",
                    "quote": "The future belongs to those who believe in the beauty of their dreams."
                },
                {
                    "name": "Maya Angelou",
                    "quote": "There is no greater agony than bearing an untold story inside you."
                },
            ]