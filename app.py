from flask import Flask,render_template,request
import sqlite3
import re
app=Flask(__name__)
conn=sqlite3.connect("users.db")
cur=conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS users(username TEXT , password TEXT)""")
conn.commit()
conn.close()
@app.route("/")
def home():
    return render_template("login.html")

@app.route("/register")
def register_page():
    return render_template("registration.html")

password=request.form["password"]
if (len(password)>=8 and
    re.search("[a-z]",password)and
    re.search("[A-Z]",password)and
    re.search("[0-9]",password)and
    re.search("[@#$&*%!]",password)):

    return "Strong Password.."
else:
    return "Password Must Contain Uppercase,Lowercase,Number and Special Character"
    
@app.route("/register",methods=["POST"])
def register():
    username=request.form["username"]
    email=request.form["email"]
    password=request.form["password"]

    conn=sqlite3.connect("users.db")
    cur=conn.cursor()

    cur.execute("INSERT INTO users VALUES(?,?)",(username,password))

    conn.commit()
    conn.close()

    return f"Registered Successfully {username}"

@app.route("/login",methods=["POST"])
def login():
    username=request.form["username"]
    password=request.form["password"]

    conn=sqlite3.connect("users.db")
    cur=conn.cursor()

    cur.execute("SELECT * FROM users WHERE username=? AND password=?",(username,password))

    user=cur.fetchone()

    conn.close()
    if user:
        return f"""
            <script>
            window.location.href='/home';</script>"""
    else:
        return "Invalid Login or Password"

@app.route("/quiz")
def quizp():
    return render_template("quz.html")

@app.route("/home")
def homepage():
    return render_template("home.html")
if __name__ == "__main__":
    app.run(debug=True)
