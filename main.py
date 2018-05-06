from flask import request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from models import Blog, User
from app import app, db
import cgi

@app.before_request
def require_login():
    allowed_routes = ['log_in', 'single_entry', 'sign_up', 'index', 'go_home', 'all_blog']
    if request.endpoint not in allowed_routes and 'username' not in session:

        return redirect('/login')


@app.route('/newpost', methods=['POST', 'GET'])
def add_post():   
    
    if request.method == 'POST':
        title = request.form['post-title']
        body = request.form['post-body']
        #username = User.query.filter_by().first()

        if title == "" or body == "":
            flash("""Error: Please fill all fields""", 'error') 
            return render_template('newpost.html', title=title, body=body)#, validation_error=validation_error, title=title, body=body)

        else:
            owner = User.query.filter_by(username=session['username']).first()
            new_post = Blog(title, body, owner)
            db.session.add(new_post)
            db.session.commit()
            flash('Success!')
            blog = Blog.query.all()
            blog = Blog.query.filter_by(owner=owner).all()
            #for last in blog:
                #last_post = last.id
            #return redirect('/blog?id={0}'.format(last_post))
            return redirect('/singleUser')
    else:
        id = User.query.filter_by().first()
        username = User.query.filter_by().first()

        return render_template('newpost.html', username=username.username)

@app.route('/posts', methods=['POST','GET'])
def all_blog():
    if request.method == 'GET':
        user=request.args.get('id')
        if user:
            username=User.query.filter_by(username=user).first()
            blog=username.blogs
        else:
            blog = Blog.query.all()
            
        return render_template('posts.html', blog=blog)
   
@app.route('/blog', methods=['POST','GET'])
def single_entry():
    
    if request.method == 'GET':
        blog_id=request.args.get('id')
        blog=Blog.query.filter_by(id=blog_id).first()
        return render_template('blog.html', blog=blog)
        
     
@app.route('/singleUser', methods=['POST','GET'])
def my_blog():# 
    if request.method == 'GET':
        user = User.query.filter_by(username=session['username']).first() 
        return render_template('singleUser.html', user=user)
    

@app.route('/signup', methods = ["POST", "GET"])
def sign_up():#  
    if request.method == 'POST':
        username =  request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        user_exists = User.query.filter_by(username=username).first()
        if not user_exists:
            if username == "" or password =="" or verify =="":
                fill_error = 'please fill in all areas'
                return render_template('signup.html', username=username, fill_error=fill_error)
            
            elif  " " in username or " " in password:
                username_error = 'please do not use blank spaces'
                return  render_template('signup.html', username=username, username_error=username_error)
            
            elif len(username) < 3:
                userlen_error = 'please enter a username more than 3 characters'
                return render_template('signup.html', username=username, userlen_error=userlen_error)
            
            elif len(password) < 3:
                password_error = 'please enter a password more than 3 characters'
                return render_template('signup.html', username=username,  password_error=password_error)

            elif password == verify:
                 
                new_user = User(username, password)
                    
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                flash('Logged in', 'session')
                blog = Blog.query.all()
            
                return render_template('base.html', username=username)
        
            else:
                verify_error = 'please make sure your verification matches your password!'
                return render_template('signup.html', username=username, verify_error=verify_error)  
        else:
            error = "Username exists"
            return render_template('signup.html', error=error)
    else:
        return render_template('signup.html')
@app.route('/login', methods=['POST', 'GET'])
def log_in():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if username == "" or password =="":
                flash('Please fill in all areas', "error")
                return render_template('login.html', username=username)
        elif user and user.password == password:
            session['username'] = username
            flash('Logged in', 'session')
            return redirect('/newpost')
            #return render_template('newpost.html', username=username)
        else:
            flash('Wrong Password or Ivalid User', "error")
            

            return render_template('login.html', username=username)
    else:
        return render_template('login.html')

@app.route('/logout')
def log_out():
    del session['username']
    
    return redirect('/posts')#using /login works

@app.route('/index', methods=['POST', 'GET'])
def go_home():
    
    if request.method == 'GET':
        title = request.args.get('title')
        blogs = Blog.query.all()
        user = User.query.all() 
        return render_template('index.html', blogs=blogs, user=user, title=title)
    
    #return redirect ('/')
    return render_template('index.html')
@app.route('/about') 
def read_about():
    return render_template('about.html')   

@app.route('/', methods=['POST', 'GET'])
def index():
    
    if request.method =='GET':
        id = request.args.get('id')
        username = request.args.get('username')
        title = request.args.get('title')
        if username==username:
            return render_template('base.html', id=id, username=username, title=title)
        else:
            return render_template('login')
    else:
        #username = User.query.filter_by(id=id).first()  
        return render_template('base.html')

if __name__ == '__main__':
    app.run()