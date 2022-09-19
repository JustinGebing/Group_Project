from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash

class Bill:
    def __init__(self,data) -> None:
        self.id = data['id']
        self.bill_name = data['bill_name']
        self.image = data['image']
        self.due_date = data['due_date']
        self.how_much = data['how_much']
        self.recurring = data['recurring']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data ['user_id']
    @staticmethod
    def validatebill(bill):
        is_valid = True
        if len(bill['bill_name']) < 2:
            flash("Bill Name Is A Required Field And Must Be More than 2 Characters")
            is_valid = False
        if len(bill['due_date']) < 1:
            flash("Date Is A Required Field")
            is_valid = False
        if len(bill['how_much']) < 1:
            flash("Bill Cost Is A Required Field")
            is_valid = False
        return is_valid
    @classmethod
    def addbill(cls,data):
        query = "INSERT INTO bills (bill_name,image,due_date,how_much,recurring,user_id ) VALUES (%(bill_name)s, %(image)s, %(due_date)s, %(how_much)s, %(recurring)s, NOW(), NOW(), %(user_id)s)"
        return connectToMySQL('Bills-n-Stuff').query_db(query,data)

    @classmethod
    def updatebill(clas,data):
        query = "UPDATE bills SET bill_name = %(bill_name)s, image = %(image)s, due_date = %(due_date)s, how_much = %(how_much)s, recurring = %(recurring)s, updated_at = NOW() WHERE id = %(id)s"
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
