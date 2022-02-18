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

# @app.route('/delete-post/<id>')
# @login_required
# def delete_post(id):
#     post = Post.query.filter_by(id=id)

#     if not post:
#         flash("This post has been 86'd", "error")
#     elif current_user.id != post.id:
#         flash('Sorry! You cannot delete this post!','error')
#     else:
#         post.delete_post()
#         flash('86 That Post','success') 

@app.route('/delete-post/<int:post_id>')
@login_required
def delete_post(post_id):
    if not current_user:
        flash('Sorry, You cannot change this!')
        return redirect(url_for('blog'))
    post = Post.query.get_or_404(post_id)
    post.delete_post()
    flash('The Post Has been Deleted', 'success')
    return redirect(url_for('blog'))
 
   

@app.route('/post/<int:post_id>', methods=["GET","POST"])
def about_post(post_id):
    #get the post or show an error (404)
    post = Post.get_or_404(post_id)
    
    return render_template('post.html', post = post)

@app.route('/posts/<int:post_id>/edit', methods=["GET","POST"])
@login_required
def editPost(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm()

    if current_user.id != post.user_id:
        flash("Sorry! You cannot edit this one!", "danger")
        return redirect(url_for ('blog.html', post_id =post.id))

    if form.validate_on_submit():
        post.title = form.title.data
        post.body= form.body.data

        post.save()
        flash('Your Post Has Been Updated!','primary')
        return redirect(url_for('blog.html', post_id = post.id))
    return render_template('editPost.html',post=post,form=form)
   