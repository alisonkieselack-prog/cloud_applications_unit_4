from functools import wraps
from flask import session, redirect, flash

def login_required(f):
    wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash('Please log in to submit a book.', 'fail')
            return redirect("/sessions/new")
        return f(*args, **kwargs)
    return decorated_function
