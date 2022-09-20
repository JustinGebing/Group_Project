from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_app.models.account import Account
from flask_app.models.bill import Bill
from flask_bcrypt import Bcrypt
bcrypt=Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=["POST"])
def process():
    if not Account.validate_account(request.form):
        return redirect('/')

    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)

    data = {
        'first_name': request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'password': pw_hash,
        }
    
    account = Account.save(data)
    session['id'] = account
    flash(f'{request.form["email"]}, you have registered!')
    return redirect('/dashboard')

@app.route('/delete/<int:id>')
def delete(id):
    Account.delete(
        {'id': id}
    )
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    data = {
        'email' : request.form['email'],
        }


    account = Account.get_one_email(data)
    if account:
        if not bcrypt.check_password_hash(account.password, request.form['password']):
            flash('Email or Password is incorect!')
            return redirect('/')
    
        session['id'] = account.id
        flash(f'{account.first_name}, you have successfully logged in!')
        return redirect('/dashboard')

    flash('Email not recognized')
    return redirect('/')

#Route to Dashboard
@app.route('/dashboard')
def dashboard():
    if 'id' not in session:
        return redirect('/logout')
    data = {
        'id': session['id']
    }
    return render_template('home.html', account=Account.get_one(data))
    # , bill=Account.getbills()

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

