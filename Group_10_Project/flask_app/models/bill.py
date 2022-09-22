from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask_app.models.account import Account
from flask import flash

class Bill:
    db = 'Bills-n-Stuff'
    def __init__(self,data) -> None:
        self.id = data['id']
        self.name = data['name']
        self.image = data['image']
        self.due_date = data['due_date']
        self.amount = data['amount']
        self.recurring = data['recurring']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.account_id = data ['account_id']
        self.account = None

    @staticmethod
    def validatebill(bill):
        is_valid = True
        if len(bill['name']) < 2:
            flash("Bill Name Is A Required Field And Must Be More than 2 Characters")
            is_valid = False
        if len(bill['due_date']) < 1:
            flash("Date Is A Required Field")
            is_valid = False
        if (bill['amount']) == "" :
            flash("Bill Cost/Amount Is A Required Field")
            is_valid = False
        return is_valid

    @classmethod
    def addbill(cls,data):
        query = "INSERT INTO bills (name,image,due_date,amount,recurring,account_id ) VALUES (%(name)s, %(image)s, %(due_date)s, %(amount)s, %(recurring)s, %(account_id)s)"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def updatebill(cls,data):
        query = "UPDATE bills SET name = %(name)s, image = %(image)s, due_date = %(due_date)s, amount = %(amount)s, recurring = %(recurring)s WHERE id = %(id)s"
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def getbill(cls,data):
        query = "SELECT * FROM bills WHERE id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query,data)
        bill = cls(results[0])
        return bill
    
    @classmethod
    def deletebill(cls,data):
        query = "DELETE FROM bills WHERE id = %(id)s"
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def getallbills(cls):
        query = "SELECT * FROM bills JOIN accounts ON bills.account_id=accounts.id;"
        results = connectToMySQL(cls.db).query_db(query)
        bills = []
        for row in results:
            bill = cls(row)
            account_data = {
                'id' : row['accounts.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'password' : row['password'],
                'created_at': row['accounts.created_at'],
                'updated_at' : row['accounts.updated_at']
            }
            account = Account(account_data)
            bill.account = account
            bills.append(bill)
        if len(results) < 1:
            return False
        return bills
        
        
