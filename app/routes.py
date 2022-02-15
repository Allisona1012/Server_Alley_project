
from app import app 
from flask import render_template,url_for,flash

from app.forms import LoginForm, RegistrationForm


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    return render_template('register.html', form = form)

@app.route('/login',methods=['GET','POST'] )
def login():
    form = LoginForm()
    return render_template('login.html', form = form)

