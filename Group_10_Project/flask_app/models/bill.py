from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash

class Bill:
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
    @staticmethod
    def validatebill(bill):
        is_valid = True
        if len(bill['name']) < 2:
            flash("Bill Name Is A Required Field And Must Be More than 2 Characters")
            is_valid = False
        if len(bill['due_date']) < 1:
            flash("Date Is A Required Field")
            is_valid = False
        if len(bill['amount']) < 1:
            flash("Bill Cost/Amount Is A Required Field")
            is_valid = False
        return is_valid
    @classmethod
    def addbill(cls,data):
        query = "INSERT INTO bills (name,image,due_date,amount,recurring,account_id ) VALUES (%(name)s, %(image)s, %(due_date)s, %(amount)s, %(recurring)s, NOW(), NOW(), %(account_id)s)"
        return connectToMySQL('Bills-n-Stuff').query_db(query,data)

    @classmethod
    def updatebill(clas,data):
        query = "UPDATE bills SET name = %(name)s, image = %(image)s, due_date = %(due_date)s, how_much = %(amount)s, recurring = %(recurring)s, updated_at = NOW() WHERE id = %(id)s"
        return connectToMySQL('Bills-n-Stuff').query_db(query,data)

    @classmethod
    def getbill(cls,data):
        query = "SELECT * FROM bills WHERE id = %(id)s"
        results = connectToMySQL('Bills-n-Stuff').query_db(query,data)
        bill = cls(results[0])
        return bill
    
    @classmethod
    def deletebill(cls,data):
        query = "DELETE FROM bills WHERE id = %(id)s"
        return connectToMySQL('Bills-n-Stuff').query_db(query,data)
