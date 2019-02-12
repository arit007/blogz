from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True      
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Blogging01@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'nachocheese'

class Blog(db.Model):    
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    
    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    posts = Blog.query.all()
    post_id = request.args.get("id")
    if post_id:
        post = Blog.query.get(post_id)
        return render_template("selectedpost.html", post=post)
        return render_template("blog.html", posts=posts)

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
        #title_error = ""
        #body_error = ""
    if request_method == "POST":
        title = request.form['title']
        body = request.form['body']
        if title == "":
                #title_error = "Please title your blog post"
            flash("Please title your blog post")
            return redirect ('/newpost')
        if body == "":
                #body_error = "Please make your blog post"
            flash("Please don't leave your post empty")
            return redirect('/newpost')
        if len(title) > 0 and len(body) > 0:
            new_post = Blog(title, body)
            db.session.add(new_post)
            db.session.commit()
            post.url = "/blog?id" + str(new_post.id)   
            return redirect(post_url)
    return render_template("newpost.html", title_error=title_error, body_error=body_error)        
 
@app.route('/')
def index():
    return redirect('/blog')

if __name__ == '__main__':
    app.run()


