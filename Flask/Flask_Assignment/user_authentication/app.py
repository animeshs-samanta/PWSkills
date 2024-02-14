from flask import Flask, render_template,request
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register')
def newAccount():
    return render_template("register.html")



#Add the user to the database
@app.route('/createaccount', methods=["POST", "GET"])
def createAccount():
    msg = "msg"
    if request.method == "POST":
        try:
            userName = request.form["userName"]
            password = request.form["password"]

            with sqlite3.connect("User.db") as con:
                cur = con.cursor()
                
                # Check if the username already exists in the database
                user_exists = cur.execute("SELECT * FROM loginInformation WHERE userName = ?", (userName,)).fetchone()

                if user_exists:
                    msg = "Username already exists. Choose another username."
                else:
                    # Insert the new user into the database
                    cur.execute("INSERT INTO loginInformation (userName, password) VALUES (?, ?)", (userName, password))
                    con.commit()
                    msg = "Account created successfully"

        except Exception as e:
            con.rollback()
            msg = "Something went wrong: " + str(e)

        finally:
            # Return the message to the client
            return msg



@app.route('/login')
def login():
    return render_template("login.html")

#Login your account 
@app.route('/loginaccount', methods=["POST", "GET"])
def loginAccount():
    msg = "msg"
    if request.method == "POST":
        try:
            userName = request.form["userName"]
            password = request.form["password"]
        
            with sqlite3.connect("User.db") as con:
                cur = con.cursor()
                #Fetch the user entered password
                check_pass = cur.execute("SELECT password FROM loginInformation WHERE userName = ?", (userName,)).fetchone()

                if check_pass and password == check_pass[0]:
                    msg = "Login successful"
                    print("Success")
                else:
                    msg = "Login Unsuccessful"
                    print("Failure")

        except Exception as e:
            con.rollback()
            msg = "Something went wrong: " + str(e)

        finally:
            return msg
            

#View the employee details 
@app.route('/view')
def viewDetails():
    con = sqlite3.connect("User.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from loginInformation")
    rows = cur.fetchall()
    return render_template("view.html", rows = rows)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
