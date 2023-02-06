from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt(app)


@app.route('/')
def login_page():
    return render_template('index.html')