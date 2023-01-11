from flask import Flask, render_template, request, url_for, flash, redirect, make_response
from moduls.db import *
import jwt
import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = '1ffad233f8a502dd24158524abd6a06031d5c5a5987df0d0'


def verify(token):
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
        if data['user'] != '':
            return True
        else:
            return False
    except:
        login()


def gen_token(user, passwd):
    id = get_id(user, passwd)
    token = jwt.encode({'id': str(id), 'user': user, 'exp': datetime.datetime.utcnow(
    ) + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
    return token


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if check_login(request.form['username'], request.form['password']):
            token = gen_token(
                request.form['username'], request.form['password'])
            resp = make_response(render_template('index.html'))
            resp.set_cookie('Auth', token)
            return resp
        else:
            error = 'Invalid Credentials. Please try again.'
            flash(error)
    else:
        print('Err')
    return render_template('login.html')


@app.route('/')
def index():
    messages = ['Hello World']
    return render_template('index.html', messages=messages)


@app.route('/about', methods=['GET'])
def about():
    if verify(request.cookies.get('Auth')):
        data = "login success!"
        return render_template('about.html', data=data)
    else:
        return redirect(url_for('login'))


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if verify(request.cookies.get('Auth')):
        token = request.cookies.get('Auth')
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
        id = data['id']
        if request.method == 'GET':
            user = get_info(id)[1]
            decription = get_info(id)[3]
            return render_template('profile.html', user=user, decription=decription)
        elif request.method == 'POST':
            print(request.form['decription'])
            update_info(id, request.form['password'],
                        request.form['decription'], request.form['address'])
            user = get_info(id)[1]
            decription = get_info(id)[3]
            address = get_info(id)[4]
            return render_template('profile.html', user=user, decription=decription, address=address)
    else:
        return redirect(url_for('login'))


def check_fill(user, passwd):
    if user != "" and passwd != "":
        return True
    else:
        return False


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        if check_fill(request.form['username'], request.form['password']):
            if check_doub(request.form['username']):
                error = 'Username already exists'
                flash(error)
            else:
                mycursor.execute("INSERT INTO users (user, password) VALUES (%s, %s)",
                                 (request.form['username'], request.form['password']))
                mydb.commit()
                return redirect(url_for('login'))
        else:
            flash('Please fill in all fields')
    elif request.method == 'GET':
        return render_template('register.html')
    return render_template('register.html')
