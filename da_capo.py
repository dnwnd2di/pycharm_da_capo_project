from flask import Flask, render_template, request, make_response, url_for, session, g, redirect
from flask.ext.mysql import MySQL
from werkzeug.security import check_password_hash, generate_password_hash
import json

app = Flask(__name__)

@app.route('/')
def base_test():
    return render_template('style.html')


if __name__ == "__main__":
    app.run()
