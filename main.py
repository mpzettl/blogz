from flask import request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from models import Blog, User
from app import app, db
import cgi




@app.route('/validation', methods=['POST', 'GET'])
def validation():
    
    
    validation_error = """Error: Please fill all fields""" 


    return render_template('newpost.html', validation_error=validation_error)




@app.route('/newpost', methods=['POST', 'GET'])
def add_post():   
    
    if request.method == 'POST':
        title = request.form['post-title']
        body = request.form['post-body']
        username = User.query.filter_by().first()


        if title == "" or body == "":
            validation_error = """Error: Please fill all fields"""
            return render_template('newpost.html', validation_error=validation_error, title=title, body=body)

        else:
            new_post = Blog(title, body)
            
            db.session.add(new_post)
            db.session.commit()
            blog = Blog.query.all()
            for last in blog:
                last_post = last.id

            
            return redirect('/blog?id={0}'.format(last_post))
        
    else:
        id = User.query.filter_by().first()
        username = User.query.filter_by().first()

        #username=username.username
        return render_template('newpost.html', username=username.username)

@app.route('/posts', methods=['POST','GET'])
def my_blog():
    username = User.query.filter_by().first()
    if request.method == 'GET':
        blog = Blog.query.all()
        username=username.username 
        return render_template('posts.html', blog=blog, username=username)
    else:
        return render_template('posts.html')
@app.route('/blog', methods=['POST','GET'])
def single_entry():
    if request.method == 'GET':
        username = request.args.get('username')
        entry = request.args.get('id')
        blog = Blog.query.filter_by(id=entry).first()

        return render_template('blog.html', blog=blog)
    else:
        
        
        return render_template('posts.html')  

@app.route('/signup', methods = ["POST", "GET"])
def sign_up():
    
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
        
        if user and user.password == password:
            
            return redirect('/')
            #return render_template('newpost.html', username=username)
        else:
            error = "Password incorrect or user does not exist"

            return render_template('login.html', username=username, error=error)
    else:
        return render_template('login.html')

@app.route('/logout')
def log_out():
    #del session['username']
    
    return redirect('/login')

@app.route('/home', methods=['POST', 'GET'])
def go_home():

    return redirect ('/')
    
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