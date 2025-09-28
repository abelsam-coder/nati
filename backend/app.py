from flask import Flask,render_template,request,session
from flask_bcrypt import Bcrypt,generate_password_hash,check_password_hash
import sqlite3,base64,mimetypes
app = Flask(__name__,template_folder="../template")
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

@app.route('/add/service',methods=["POST","GET"])
def service():
    if request.method == "POST":
        name = request.form["name"]
        
        photo = request.form["photo"]
        price = request.form["price"]
        per = request.form["per"]
        des = request.form["des"]
        filetype,_ = mimetypes.guess_extension(photo.filename)
        encode = base64.b64encode(photo.read()).decode()
        h = f"data:{filetype};base64,{encode}"
        db = sqlite3.connect('../database/database.db')
        cursor = db.cursor()
        cursor.execute("INSERT INTO service (name , photo , price , per , des) VALUES(?,?,?,?,?)",(name,h,price,per,des))
        db.commit()
    return render_template("serviceadd.html")

@app.route('/comment',methods=["POST","GET"])
def comment():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        feedback = request.form["feedback"]
        phone = request.form["phone"] 
        db = sqlite3.connect('../database/database.db')
        cursor = db.cursor()
        cursor.execute("INSERT INTO comment (username,email,phone,feedback) VALUES(?,?,?,?)",(username,email,phone,feedback))
        db.commit()
    return render_template("comment.html")

@app.route('/admin/comments')
def comments():
    db = sqlite3.connect('../database/database.db')
    cursor = db.cursor()    
    cursor.execute("SELECT * FROM comment")
    fetch = cursor.fetchall()
    return render_template("comments.html",fetch=fetch) 

@app.route('/admin/users') 
def users():
    db = sqlite3.connect('../database/database.db')
    cursor = db.cursor()    
    cursor.execute("SELECT * FROM users")
    fetch = cursor.fetchall()
    return render_template("users.html",fetch=fetch) 

# @app.route('/cart',methods=["POST","GET"])
# def cart():
#     db = sqlite3.connect('../database/database.db')
#     cursor = db.cursor()  
#     cursor.execute("INSERT INTO cart")

if __name__ == "__main__":
    app.run()        