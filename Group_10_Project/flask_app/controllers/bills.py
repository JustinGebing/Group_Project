from email.mime import image
from unittest import result
from urllib import response
from flask import render_template, redirect, session, request, flash, jsonify,json
from flask_app import app
from flask_app.models.bill import Bill
from flask_app.models.account import Account
from flask_app.models.image_text import Image_text
import os


#New route to render create bill page
@app.route('/new/bill')
def new_bill_page():
    if 'id' not in session:
        return redirect('/logout')
    if Bill.validatebill(request.form):
        print(request.form['account_id'])
        Bill.addbill(request.form)
    session['check']="1"
    data = {
        'id':session['id']
    }
    if request.method == "POST":
        images = request.files['file']
        filename=images.filename
        session['total_cost']=Image_text.total_amount(images,filename)
    return render_template('create.html', account=Account.get_one(data))

#Route to create bill
@app.route('/create/bill', methods=['POST'])
def create_bill():
    if 'id' not in session:
        return redirect('/logout')
    # if session['check']=="1":
    #     total_cost=""
    #     filelocation=""
    #     images = request.files['file']
    #     filename=images.filename
    #     filelocation="c:/fakepath/flask_app/static/img"+filename
    #     print("File Location:"+filelocation)
    #     session['image_location']=filelocation
    #     print(filelocation)
    #     total_cost=Image_text.total_amount(images,filename)
    #     session['total_cost']=total_cost
    #     print(session['total_cost'])
    #     session['check']="0"
    #     return render_template('create.html',total_cost=session['total_cost'],image_loc=session['image_location'])
    # elif not Bill.validatebill(request.form):
    #     return redirect('/new/bill')
    # session['check']="1"
    data = {
        'name': request.form['name'],
        'image': request.form.get('image', False),
        'due_date': request.form['due_date'],
        'amount': request.form['amount'],
        'recurring': request.form.get('recurring', False),
        'account_id': request.form['account_id']
    }
    Bill.addbill(data)
    # os.remove(session['image_location']) 
    return redirect('/dashboard')


#Route to show bill
@app.route('/bill/<int:id>')
def show_bill(id):
    if 'id' not in session:
        return redirect('/logout')
    bill_data = {
        'id': id
    }
    bill = Bill.getbill(bill_data)
    return render_template('show.html', bill=bill)

#Route to edit page
@app.route('/edit/bill/<int:id>')
def edit_page(id):
    if 'id' not in session:
        return redirect('/logout')
    bill_data = {
        'id': id
    }
    bill = Bill.getbill(bill_data)
    return render_template('edit.html', bill=bill)

#Route to edit bill
@app.route('/update/bill/<int:id>', methods=['POST'])
def update_bill(id):
    if 'id' not in session:
        return redirect('/logout')
    data = {
        'id' : request.form['id'],
        'name' : request.form['name'],
        'amount' : request.form['amount'],
        'recurring' : request.form.get('recurring', False),
        'due_date' : request.form['due_date'],
        'image' : request.form.get('image', False)
    }
    Bill.updatebill(data)
    return redirect(f'/edit/bill/{id}')

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


