from flask import Flask, render_template

app = Flask(__name__)

# Route for the home page
@app.route('/')
def home():
    return 'Welcome to my Flask app!'

# Custom 404 error handler
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

# Custom 500 error handler
@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
