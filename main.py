from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True      
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Blogging01@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'nAcHoChEeS3'

class Blog(db.Model):    
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    
    def __init__(self, title, body):
        self.title = title
        self.body = body
       
#display all blog posts
@app.route('/blog', methods=['POST', 'GET'])
def blog():
    blog_id = request.args.get('id')
    blogs = Blog.query.all()
    if blog_id is None:
        return render_template('blog.html', blogs=blogs)
    else: 
        
        blog = Blog.query.get(blog_id) #changed from blogs to blog
        return render_template('selectedpost.html', blog=blog)

#after submitting new post display on main blog page    
@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        if title and body == "":
            flash("Please don't leave post empty")
            return redirect('/newpost')
        else:
            new_blog = Blog(title, body)
            db.session.add(new_blog)
            db.session.commit()
        blogs = Blog.query.all()
        return render_template('blog.html', blogs=blogs)   
    return render_template("newpost.html")    
 
@app.route('/', methods =['POST', 'GET'])
def index():
    if request.method == 'POST':
        blog_name = request.form['blog']
        new_blog = Blog(blog_name)
        db.session.add(new_blog)
        db.session.commit()
    blogs = Blog.query.all()
    return render_template('blog.html', blogs=blogs)    
   
if __name__ == '__main__':
    app.run()


