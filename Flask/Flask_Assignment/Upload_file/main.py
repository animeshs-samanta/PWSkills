from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def show_form():
    return render_template("index.html")

@app.route('/success', methods = ['POST'])   
def success():   
    if request.method == 'POST':   
        f = request.files['file'] 
        f.save(f.filename)   
        return render_template("success.html", name = f.filename)

if __name__ == "__main__" :
    app.run(host="0.0.0.0", port=5000)

