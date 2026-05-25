from flask import Flask,render_template,request,session
import sqlite3
import re
app=Flask(__name__)
app.secret_key="anquiz"
conn=sqlite3.connect("users.db")
cur=conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS users(username TEXT , password TEXT) , email TEXT""")
conn.commit()
conn.close()

conn=sqlite3.connect("question.db")
cur=conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS questions(id INTEGER PRIMARY KEY AUTOINCREMENT,

subjectname TEXT,

question TEXT,
option1 TEXT,
option2 TEXT,
option3 TEXT,
option4 TEXT,

answer TEXT
)""")
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
@app.route("/admin")
def admin():
    return render_template("admin.html")
@app.route("/addquestion", methods=["POST"])
def addquestion():
    subjectname=request.form["subjectname"]
    question=request.form["question"]
    option1=request.form["option1"]
    option2=request.form["option2"]
    option3=request.form["option3"]
    option4=request.form["option4"]
    answer=request.form["answer"]
    conn=sqlite3.connect("question.db")
    cur=conn.cursor()
    cur.execute("""
    INSERT INTO questions(subjectname,question,option1,option2,option3,option4,answer)
    VALUES(?,?,?,?,?,?,?)""",(subjectname,question,option1,option2,option3,option4,answer))
    conn.commit()
    conn.close()

    return"""<script>
    alert("Question Added Successfully");
    window.location.href='/admin';
    </script>"""

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
          

'''@app.route("/quiz")
def quizp():
    if "user" in session:
        return render_template("quz.html")
    else:
        return"""
        <script>
        alert("please Login First");
        window.location.href='/login';
        </script>"""
'''
@app.route("/quiz/<subjectname>/<int:limit>/<int:minutes>")
def quizp(subjectname , limit , minutes):
    if "user" in session:
        conn=sqlite3.connect("question.db")
        cur=conn.cursor()

        cur.execute(
            """SELECT * FROM questions WHERE subjectname=? ORDER BY RANDOM() LIMIT ?""",(subjectname,limit))
        questions=cur.fetchall()

        conn.close()

        quiz_data=[]

        for q in questions:
            quiz_data.append({
                "q":q[2],
                "options":[q[3],q[4],q[5],q[6]],
                "answer":q[7],
                "attempted":False,
                "review":False
                })

        return render_template("quz.html",
                               questions=quiz_data,
                               subjectname=subjectname,
                               minutes=minutes)
    else:
        return """<script>
        alert("Please Login First");
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
