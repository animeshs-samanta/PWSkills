from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def show_form():
    return render_template("index.html")


@app.route("/user_input", methods = ['GET','POST'])
def user_input():
    name = request.form.get("name")
    mail = request.form.get("email")
    return f"Name: {name} \n\nEmail: {mail}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)