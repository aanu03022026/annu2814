from flask import Flask,render_template,request,session
import sqlite3
import re
app=Flask(__name__)
app.secret_key="anquiz"
conn=sqlite3.connect("users.db")
cur=conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS users(username TEXT , password TEXT)""")
conn.commit()
conn.close()
@app.route("/")
def home():
    return render_template("home.html")
@app.route("/register")
def register_page():
    return render_template("registration.html")
@app.route("/register",methods=["POST"])
def register():
    username=request.form["username"]
    email=request.form["email"]
    password=request.form["password"]

    password=request.form["password"]
    if not(len(password)>=8 and
            re.search("[a-z]",password)and
            re.search("[A-Z]",password)and
            re.search("[0-9]",password)and
            re.search("[@#$&*%!]",password)):
        return "Password Must Contain Uppercase,Lowercase,Number and Special Character"

    conn=sqlite3.connect("users.db")
    cur=conn.cursor()

    cur.execute("INSERT INTO users VALUES(?,?)",(username,password))

    conn.commit()
    conn.close()

    return f"Registered Successfully {username}"
@app.route("/login")
def login_page():
    return render_template("login.html")
        

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
        session["user"]=username
        return f"""
            <script>
            alert("Welcome" +"{username}");
            window.location.href='/home';</script>"""
    else:
        return"""
    <script>
    alert("Invalid Login or Password , Please Try Again With Correct One")
    window.location.href='/';
    </script>"""
          

@app.route("/quiz")
def quizp():
    if "user" in session:
        return render_template("quz.html")
    else:
        return"""
        <script>
        alert("please Login First");
        window.location.href='/login';
        </script>"""

@app.route("/home")
def homepage():
    if "user" in session:
        return render_template("home.html" , username=session["user"])
    else:
        return """ <script>
        alert("Please Login First");
        window.location.href='/login';
        </script>"""

@app.route("/logout")
def logout():
    session.pop("user",None)

    return  """
    <script>
    alert("Logged Out");
    window.location.href='/';
    </script>
    """
if __name__ == "__main__":
    app.run(debug=True)
