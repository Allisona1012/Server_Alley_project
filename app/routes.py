from app import app 
from flask import render_template,url_for,flash, redirect
from flask_login import  login_required, login_user, logout_user, current_user
from app.forms import LoginForm, PostForm, RegistrationForm
from app.models import User, Post


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        print('The form has been Validated!')
        username= form.username.data
        email= form.email.data 
        password= form.password.data 

        user_exists = User.query.filter((User.username == username ) | (User.email == email)).all()
        if user_exists:
            flash('User with username {username} or email {email} already exists', 'danger')
            return redirect(url_for('register'))

        #create a new User
        User(username=username, email = email, password= password)
        flash('Thank you for registering!','primary')
        return redirect(url_for('index'))
    return render_template('register.html', form = form )

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        
        # Grab the data from the form
        username = form.username.data
        password = form.password.data
       
        # Query user table for user with username
        user = User.query.filter_by(username=username).first()
        
        # if the user does not exist or the user has an incorrect password
        if not user or not user.check_password(password):
            # redirect to login page
            flash('That username and password is incorrect')
            return redirect(url_for('login'))
        
        # if user does exist and correct password, log user in
        login_user(user)
        flash('You have successfully been logged in', 'success')
        return redirect(url_for('index'))
        
    return render_template('login.html', form =form )

@app.route('/logout')
def logout():
    logout_user()
    flash('You have sucessfully logged out.', 'error')
    return redirect(url_for('index')) 

@app.route('/blog')
def blog():
    #show the posts the users have created
    posts= Post.query.all()
    return render_template('blog.html', posts = posts)


@app.route('/make-post', methods=["GET","POST"])
#to be able to make a post someone has to be logged in
@login_required
def makePost():
    form = PostForm()

    if form.validate_on_submit():
        title= form.title.data
        body = form.body.data
        user_id= current_user.id

        Post(title=title, body=body, user_id = user_id)
        return redirect(url_for('blog', form=form))

    return render_template('makePost.html', form=form)