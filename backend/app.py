from flask import Flask,render_template,request,session
from flask_bcrypt import Bcrypt,generate_password_hash,check_password_hash
import sqlite3
app = Flask(__name__)
@app.route('/signup',methods=["POST","GET"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = sqlite3.connect('../database/database.db')
        cursor = db.cursor()
        try:
            cursor.execute("INSERT INTO users (username,password) VALUES(?,?)",(username,password))
            db.commit()
            session["username"] = username
            return 'a'
        except sqlite3.IntegrityError:
            return '<script>alert("username already exists")</script>'
    return render_template("signup.html")

@app.route('/admin/login',methods=["POST","GET"])
def admin():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = sqlite3.connect('../database/database.db')
        cursor = db.cursor()
        cursor.execute("SELECT * FROM admin WHERE username = ? AND password = ?",(username,password))
        fetch = cursor.fetchone()
        if fetch:
            return 'aaa'
        else:
            return 'f'
    return render_template("adminlogin.html")        

@app.route('/home')
@app.route('/')
def home():
    return render_template("home.html")