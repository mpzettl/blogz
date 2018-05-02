from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'
class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(4000))
    #submitted = db.Column(db.Boolean)

    def __init__(self, title, body):  
        self.title = title
        self.body = body
@app.route('/validation', methods=['POST', 'GET'])
def validation():
    
    
    validation_error = """Error: Please fill all fields""" 


    return render_template('newpost.html', validation_error=validation_error)




@app.route('/newpost', methods=['POST', 'GET'])
def add_post():   

    if request.method == 'POST':
        title = request.form['post-title']
        body = request.form['post-body']
        


        if title == "" or body == "":
            validation_error = """Error: Please fill all fields"""
            return render_template('newpost.html', validation_error=validation_error, title=title, body=body)

        else:
            new_post = Blog(title, body)
            
            db.session.add(new_post)
            db.session.commit()
            blog = Blog.query.all()
            for last in blog:
                last.id

            
            return redirect('/blog?id={0}'.format(last.id))
        
    else:

        return render_template('newpost.html')

@app.route('/posts', methods=['POST','GET'])
def my_blog():
    if request.method == 'GET':
        blog = Blog.query.all()

        return render_template('posts.html', blog=blog)
    else:
        return render_template('posts.html')
@app.route('/blog', methods=['POST','GET'])
def single_entry():
    if request.method == 'GET':
        
        entry = request.args.get('id')
        blog = Blog.query.filter_by(id=entry).first()

        return render_template('blog.html', blog=blog)
    else:
        
        
        return render_template('posts.html')  

@app.route('/', methods=['POST', 'GET'])
def index():
    
    return render_template('base.html', my_blog=my_blog)

if __name__ == '__main__':
    app.run()