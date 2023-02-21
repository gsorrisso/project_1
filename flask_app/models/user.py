from flask_app.config.mysqlconnection import connectToMySQL
#in the class apps you need this ^ written from folder to file 
from flask import flash, request
from flask_app import bcrypt
import re	# the regex module

# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email_address = data['email_address']
        self.password = data['password']
    
    
    @classmethod
    def get_id(cls, data):

        query = "SELECT * FROM users WHERE id = %(id)s;"

        results = connectToMySQL('weddingProject').query_db(query, data)
        return cls(results[0]) if results else None
    
    @classmethod
    def get_email(cls, data):

        query = "SELECT * FROM users WHERE email_address = %(email_address)s;"

        result = connectToMySQL('weddingProject').query_db(query, data)
        
        return cls(result[0]) if result else None
    
    
    @staticmethod
    def validate_registration(user_info):
        is_valid = True
        data = {
            'email_address': request.form['email_address']
        }
        if len(user_info['first_name']) <= 0:
            flash('First name required!', 'register')
            is_valid = False

        if len(user_info['last_name']) <= 0:
            flash('Last name required!', 'register')
            is_valid = False

        if len(user_info['email_address']) <= 0:
            flash('Email required!', 'register')
            is_valid = False

        if not EMAIL_REGEX.match(user_info['email_address']):
            flash('Invalid Email Address', 'register')
            is_valid = False

        if len(user_info['password']) <= 5:
            flash('Password must be at least 5 characters', 'register')
            is_valid = False

        if user_info['password'] != user_info['confirm_password']:
            flash('Passwords need to match', 'register')
            is_valid = False        
        
        if not EMAIL_REGEX.match(user_info['email_address']):
            flash('Invalid credentials','login')
            return False

        if User.get_email(data):
            flash('Email already taken', 'register')
            is_valid = False

        print('Validation: User is valid: ', is_valid)

        return is_valid
    
    
    @classmethod # this saves the data and updates the database with new information
    def save(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email_address, password) VALUES (%(first_name)s, %(last_name)s, %(email_address)s, %(password)s);'

        return connectToMySQL("weddingProject").query_db(query, data)
