from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_bcrypt import Bcrypt
import re
from flask_app.models.bill import Bill

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Account:
    db = 'Bills_n_Stuff'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.bills = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM accounts;"
        results = connectToMySQL(cls.db).query_db(query)
        accounts = []
        for row in results:
            accounts.append( cls(row) )
        return accounts

    @classmethod
    def get_one(cls, data):
        query = 'SELECT * from accounts WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        print(results[0])
        return cls(results[0])

    @classmethod
    def get_one_email(cls, data):
        query = 'SELECT * from accounts WHERE email = %(email)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        print(results[0])
        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO accounts (first_name, last_name, email, password) Values (%(first_name)s, %(last_name)s, %(email)s, %(password)s);'
        save = connectToMySQL(cls.db).query_db(query, data)
        print(save)
        return save
        

    @classmethod
    def update(cls, data):
        query = 'UPDATE accounts SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, password=%(password)s, WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = 'DELETE FROM accounts WHERE id = %(id)s'
        return connectToMySQL(cls.db).query_db(query, data)

#This Method Gets All The Bills Associated With One User
    @classmethod
    def getbills(cls):
        query = "SELECT * FROM accounts LEFT JOIN bills on accounts.id = bills.user_id"
        results = connectToMySQL(cls.db).query_db(query)
        account = cls(results[0])
        for abill in results:
            bill = {
                'id': abill['bills.id'],
                'bill_name': abill['bill_name'],
                'image':abill['image'], 
                'due_date': abill['due_date'],
                'how_much': abill['how_much'],
                'recurring': abill['recurring'],
                'created_at':abill['bills.created_at'],
                'updated_at': abill['bills.updated_at'],
                'user_id': abill['user_id']
            }
            account.bills.append(bill)
        if len(results) < 1:
            return False
        return account

    @staticmethod
    def validate_account(account):
        valid = True
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        if len(account['first_name']) < 3:
            valid = False
            flash('First name has to have at least 3 characters', 'error')
        
        if len(account['last_name']) < 3:
            valid = False
            flash('Last name has to have at least 3 characters', 'error')

        if not email_regex.match(account['email']):
            flash('Please enter a valid email address', 'error')
            valid = False

        if Account.get_one_email(account):
            flash('Email already exists', 'error')
            valid = False

        if len(account['password']) < 8 :
            flash('Password has to be at least 8 characters', 'error')
            valid = False

        if account['password'] != account['confirm_password']:
            flash("Passwords must match", 'error')
            valid = False
        
        return valid

@staticmethod
def validate_login(account):
    valid = True
    
    if not email_regex.match(account['email']):
        flash('Please enter a valid email address', 'error')
        valid = False

    return valid