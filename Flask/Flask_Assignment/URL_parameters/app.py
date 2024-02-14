from flask import Flask, render_template,request

app = Flask(__name__)

@app.route('/dynamic_param')
def dynamic_param():
    name = request.args.get('name', 'Guest')
    return render_template("dynamic_param.html",name = name)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)