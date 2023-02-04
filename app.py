from flask import Flask, render_template, send_from_directory, url_for, redirect, request, make_response
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)





@app.route("/")
def hello():
    return "Hello, Welcome to GeeksForGeeks"





 
if __name__ == "__main__":
    app.run(debug=True)