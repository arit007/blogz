from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True      
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Blogging01@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

#TODO- be sure to write an outline for each step you plan to take

class Blog(db.Model):

@app.route('/blog', methods=['POST', 'GET'])

@app.route('/newpost', methods=['POST', 'GET'])

