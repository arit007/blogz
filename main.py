from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True      
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:WorseTumblr01@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'pbandj'  

class Blog(db.Model):    
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), unique = True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'index', 'blog']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/logout')
def logout():
    del session['username']
    flash('Logged Out')
    return redirect('/blog')

@app.route('/login', methods = ['POST', 'GET'])
def login(): 
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username = username).first()
        if user and user.password == password:
            session['username'] = username
            flash('Logged In', 'error')
            return redirect('/newpost')
        elif not user:
            flash('Username does not exist', 'error')  
            return redirect('/login')  
        else:
            flash('User password incorrect', 'error')
    return render_template('login.html')

@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        existing_user = User.query.filter_by(username=username).first()
    
        if not username:
            flash('Do not leave username blank', 'error')
            return redirect('/signup')
        elif not password:
            flash('Do not leave password blank', 'error')
            return redirect('/signup')
        elif password != verify:
            flash('Password and verification do not match', 'error') 
            return redirect('/signup')   
        elif len(username)<=3 or len(password)<=3:
            flash('Username or password not long enough', 'error')
            return redirect('/signup')  
        else:
            if not verify:
                flash('Do not leave verify blank', 'error')
                return redirect('/signup')    
    
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/newpost') 
        else:
            flash('Duplicate username', 'error')
            return redirect('/signup')

    return render_template('signup.html')

#display individual users
@app.route('/', methods =['POST', 'GET'])
def index():
    user_id = request.args.get('id')
    users = User.query.all()
    if user_id is None:
        return render_template('index.html', users=users)
    else: 
        user = User.query.get(user_id) 
    return redirect('/blog?id={}'.format(user_id.id))

#display all blog posts
@app.route('/blog', methods=['POST', 'GET'])
def blog():
    blog_id = request.args.get('id')
    blogs = Blog.query.all()
    user_id = request.args.get('user')
    # if blog_id is None:
    #     return render_template('blog.html', blogs=blogs)
    # else: 
        
    #     blog = Blog.query.get(blog_id)
    #     return render_template('selectedpost.html', blog=blog)
    
    # if user_id:
    #     blog = Blog.query.filter_by(owner_id=user_id)
    #     return render_template('singleUser.html')
    if user_id:
        blogs = Blog.query.filter_by(owner_id=user_id)
        return render_template('singleUser.html', blogs=blogs, header="User Posts")
    if blog_id:
        blog = Blog.query.get(blog_id)
        return render_template('selectedpost.html', blog=blog)
    return render_template('blog.html', blogs=blogs, header="All Blog Posts")    

@app.route('/newpost', methods=['POST', 'GET'])
def new_post():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        owner = User.query.filter_by(username=session['username']).first()
        if not title:
            flash('Please dont leave post empty', 'error')
            return redirect('/newpost')
        elif not body: 
            flash('Please dont leave post empty', 'error')
            return redirect('/newpost')    
        else:
            new_blog = Blog(title, body, owner)
            db.session.add(new_blog)
            db.session.commit()
        blogs = Blog.query.all()
        #return render_template('blog.html', blogs=blogs) 
        return redirect('/blog?id={}'.format(new_blog.id))  
    return render_template("newpost.html")    
 
if __name__ == '__main__':
    app.run()

  


