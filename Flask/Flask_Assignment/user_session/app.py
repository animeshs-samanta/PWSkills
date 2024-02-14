from flask import Flask, render_template, request, session

app = Flask(__name__)

'''
import secrets
# Generate a secure random key with 32 bytes (256 bits)
secret_key = secrets.token_hex(32)
print("Generated Secret Key:", secret_key)
'''
app.secret_key = '093ce0ca2959ee2cca859868f063965722aa1d5e41634a053eaf93c3af4b125b'
@app.route('/')
def show_form():
    return render_template("home.html")


@app.route("/session_input", methods = ['GET','POST'])
def user_input():
    name = request.form.get("name")
    mail = request.form.get("email")

    session['name'] = name
    session['email'] = mail

    name = session.get('name', 'No Name')
    mail = session.get('email', 'No Email')

    return f"Name: {name} \n\nEmail: {mail}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)