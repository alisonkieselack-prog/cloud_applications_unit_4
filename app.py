from flask import Flask, render_template, request, redirect, session, flash 
from database_connection import DatabaseConnection
from book_repository import BookRepository
from book import Book
from user_repository import *
from user import *
from authenticated import *
from login_required import *

# instantiate a Flask app object
app = Flask(__name__)

app.secret_key = "extremely_secret_key"

# Declares a route that listens for a GET request to the path /hello
# and a method to execute when that request comes in
@app.route('/hello', methods=['GET'])
def hello():
    return "Hello to you too"

# @app.route("/books", methods=["GET"])
# def get_books():
#     return render_template("books.html")

@app.route('/books', methods=['GET'])
def get_all_books():
    connection = DatabaseConnection()
    connection.connect()
    book_repository = BookRepository(connection)
    books = book_repository.all()
    return render_template("books.html", books=books)

@app.route('/add_book', methods=['GET'])
def get_book_form():
    return render_template("add_book_form.html")

@app.route('/add_book', methods=['POST'])
@login_required
def create_book():
    connection = DatabaseConnection()
    connection.connect()

    book_repository = BookRepository(connection)

    book_details = request.form
    book = Book(None, book_details['title'], book_details['author'], "")
    book_repository.create(book)
    flash('Book successfully submitted!', 'success')
    return redirect("/add_book")

@app.route('/users/new', methods=["GET"])
def get_signup_form():
    return render_template("signup_form.html")

@app.route('/users/new', methods=["POST"])
def create_user():
    connection = DatabaseConnection()
    connection.connect()

    user_repository = UserRepository(connection)
    user_details = request.form
    username = user_details["username"]

    existing_user = user_repository.find_by_username(username)

    if existing_user:
        flash('Username already exists. Try logging in instead.', 'fail')
        return redirect("/sessions/new")

    else:
        new_user = User(username=user_details["username"], password=user_details["password"])
        user_repository.create(new_user)
        username = user_details["username"]
        user = user_repository.find_by_username(username)
        session['user_id'] = user.id
        session['username'] = user.username
        flash('Sign up successful!', 'success')
        return redirect("/")

@app.route('/sessions/new', methods=['GET'])
def get_login_form():
    return render_template("login_form.html")

@app.route('/sessions/new', methods=['POST'])
def create_session():
    connection = DatabaseConnection()
    connection.connect()
    user_repository = UserRepository(connection)

    username = request.form["username"]
    password = request.form["password"]

    user = user_repository.find_by_username(username)

    if user and user.password == password:
        session['user_id'] = user.id
        session['username'] = user.username
        return redirect('/books')
    else:
        flash('Incorrect username or password, please try again.', 'fail')
        return redirect('/sessions/new')

@app.route('/authors', methods=['GET'])
def get_authors():
    authors = [
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
    return authors

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route('/team', methods=['GET'])
def get_team():
    team = ["Alison", "Charlie", "Jon", "Danesh", "Syed", "Ben Meads"]
    return render_template("team.html", team=team)

@app.route('/quotes', methods=["GET"])
def get_quotes():
    quotes = [
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
    return quotes

@app.route('/quoteshtml', methods=["GET"])
def get_quoteshtml():
    return render_template("quotes.html")

@app.route('/books/<int:book_id>', methods=['GET'])
def get_individual_book(book_id):
    connection = DatabaseConnection()
    connection.connect()
    book_repo = BookRepository(connection)
    book = book_repo.find(book_id)
    return render_template('book.html', book=book)

# make the server run in response to `python app.py`
# on port 5001 (you'll learn more about what this means later)
# and use debug mode so that changing code restarts the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
