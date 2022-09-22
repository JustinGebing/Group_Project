from email.mime import image
from unittest import result
from urllib import response
from flask import render_template, redirect, session, request, flash, jsonify,json
from flask_app import app
from flask_app.models.bill import Bill
from flask_app.models.account import Account
from flask_app.models.image_text import Image_text
import os


#Route to create bill page
@app.route('/new/bill')
def new_bill():
    if 'id' not in session:
        return redirect('/logout')
    data = {
        'id': session['id']
    }
    session['check']="0"
    return render_template('create.html', account=Account.get_one(data))
        
#Route to create bill
@app.route('/create/bill', methods=['POST'])
def create_bill():
    if 'id' not in session:
        return redirect('/logout')
    if not Bill.validatebill(request.form):
        return redirect('/new/bill')
    if session['check']=="1":
        total_cost=""
        filelocation=""
        images = request.files['file']
        filename=images.filename
        filelocation="c:/fakepath/flask_app/static/img"+filename
        print("File Location:"+filelocation)
        session['image_location']=filelocation
        print(filelocation)
        total_cost=Image_text.total_amount(images,filename)
        session['total_cost']=total_cost
        print(session['total_cost'])
        session['check']="0"
        return redirect('/new/bill')
    session['check']="1"
    data = {
        'name': request.form['name'],
        'image': request.form.get('image', FALSE),
        'due_date': request.form['due_date'],
        'amount': request.form['amount'],
        'recurring': request.form.get('recurring', FALSE),
        'account_id': request.form['account_id']
    }
    Bill.addbill(data)
    os.remove(session['image_location']) 
    return redirect('/dashboard')


#Route to show bill
@app.route('/bill/<int:id>')
def show_bill(id):
    if 'id' not in session:
        return redirect('/logout')
    data = {
        'id': id
    }
    account_data = {
        'id': session['id']
    }
    return render_template('show.html', bill=Bill.getbill(data), account=Account.get_one(account_data))

#Route to edit page
@app.route('/edit/bill/<int:id>')
def edit_page(id):
    if 'id' not in session:
        return redirect('/logout')
    data = {
        'id': id
    }
    account_data = {
        'id': session['id']
    }
    return render_template('edit.html', bill=Bill.getbill(data), account=Account.get_one(account_data))

#Route to edit bill
@app.route('/update/bill', methods=['POST'])
def update_bill():
    if 'id' not in session:
        return redirect('/logout')
    if not Bill.validatebill(request.form):
        return redirect('/edit/bill/<int:id>')
    data = {
        'name': request.form['name'],
        'amount': int(request.form['amount']),
        'recurring': request.form['recurring'],
        'due_date': request.form['due_date'],
        'image': request.form['image'],
        'bills': request.form['bills']
    }
    Bill.updatebill(data)
    return redirect('/dashboard')

#Route to delete bill
@app.route('/delete/bill/<int:id>')
def delete_bill(id):
    if 'id' not in session:
        return redirect('/logout')
    data = {
        'id': id
    }
    Bill.deletebill(data)
    return redirect('/dashboard')


