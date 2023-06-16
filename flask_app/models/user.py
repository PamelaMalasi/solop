from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
mydb = 'pypie_derby'

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
# route.py
class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def save(cls,data):
        query = '''
        INSERT INTO users(first_name,last_name,email,password)
        VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);
        '''
        return connectToMySQL(mydb).query_db(query,data)
    
    @classmethod
    def get_by_id(cls,data):
        query = '''
        SELECT *
        FROM users
        WHERE id = %(id)s;
        '''
        result = connectToMySQL(mydb).query_db(query,data)
        print(result)
        return cls(result[0])

    @classmethod
    def get_by_email(cls,data):
        query = '''SELECT * FROM users WHERE email = %(email)s;'''
        result = connectToMySQL(mydb).query_db(query,data)
        print(result)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user['first_name']) < 3:
            flash('First name must be at least 3 letters long.', 'register')
            is_valid = False
        if not user['first_name'].isalpha():
            flash('First name can only contain letters.', 'register')
            is_valid = False
        if len(user['last_name']) < 3:
            flash('Last name must be at least 3 letters long.', 'register')
            is_valid = False
        elif not user['last_name'].isalpha():
            flash('Last name can only contain letters.', 'register')
            is_valid = False
        if len(user['email']) < 1:
            is_valid = False
            flash('Email required', 'register')
        elif not EMAIL_REGEX.match(user['email']):
            flash('Invalid email address.', 'register')
            is_valid = False
        if len(user['password']) < 8:
            flash('Password must have at least 8 characters.', 'register')
            is_valid = False
        elif user['confirm_password'] != user['password']:
            flash('Passwords do not match.', 'register')
            is_valid = False
        this_user = User.get_by_email(user)
        if this_user:
            is_valid = False
            flash('Email already exists.', 'register')
        return is_valid

