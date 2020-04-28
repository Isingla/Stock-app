from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "<h1>Hello World</h1>"


@app.route("/about")
def about_page():
    return '<h1 style="color: red">This is the about page</h1>'


app.run()
