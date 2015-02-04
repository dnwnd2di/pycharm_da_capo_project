# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, make_response, url_for, session, g, redirect
from flask.ext.mysql import MySQL
from werkzeug.security import check_password_hash, generate_password_hash
import json

# configuration
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASK EXAMPLE_SETTINGS', silent=True)

mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
#app.config['MYSQL_DATABASE_PASSWORD'] = 'alsu12345'
app.config['MYSQL_DATABASE_PASSWORD'] = 'dlguswn12'
app.config['MYSQL_DATABASE_DB'] = 'da_capo'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)



def connect_db():
    return mysql.connect()


def init_db():
    """Creates the database tables."""
    db = connect_db()

    with app.open_resource('dacapo_wb.sql', mode='r') as f:
        sql_statements = " ".join(f.readlines())
        for sql in sql_statements.split(";"):
            if not sql:
                cursor = db.cursor()
                cursor.execute(sql)
                cursor.close()
    db.close()


def query_db(query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    g.db.execute(query, args)
    data = g.db.fetchall()
    rv = [dict((g.db.description[idx][0], value)
               for idx, value in enumerate(row)) for row in data]
    return (rv[0] if rv else None) if one else rv

@app.before_request
def before_request():
    print ("Start Application")
    db_connect = connect_db()
    db_connect.autocommit(1)

    g.db = db_connect.cursor()
    print type(g.db)

    g.user = None
    if 'user_id' in session:
        g.user = query_db('select * from User where StudentID = %s',
                          [session['user_id']], one=True)

@app.route('/login')
def login():
    if g.user:
        return redirect(url_for('information'))

    return render_template('login.html')


@app.route('/logout_process')
def logut_process():
    if g.user:
        session.pop('user_id', None)

    return render_template('login.html')

@app.route('/check_login',  methods=["POST"])
def login_check():
    if request.method == "POST":
        id = request.form['id']
        password = request.form['password']

        user = query_db('''select * from User where StudentID = %s''', [id], one=True)

        if user == None:
            error = 'Invalid UserName'
            return render_template('login.html', error=error)
        if check_password_hash(user['UserPassword'], request.form['password']):
            session['user_id'] = user['StudentID']
            return redirect(url_for('information'))
        else:
            error = 'Invalid password'
            return render_template('login.html', error=error)


    # user = query_db('''select * from user where email = %s''', [request.form['email']], one=True)
    #
    # if user is None:
    #     error = 'Invalid username'
    # elif not check_password_hash(user['password'], request.form['password']):
    #     error = 'Invalid password'
    # else:
    #     session['user_id'] = user['email']
    #     return redirect(url_for('server_list'))

    # return  render_template('login.html', error=error)

    return id + " "  + password

@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/registerUser', methods=["POST"])
def insert_new_user():
    if request.method == "POST":
        id = request.form['id']
        name = request.form['username']
        password = generate_password_hash(request.form['password'])
        email = request.form['email']
        student = query_db('''select * from Students where StudentID = %s ''', [id], one=True)

        if not request.form['id']:
            error = 'please input id'
            return render_template('register.html', error=error)
        elif not request.form['username']:
            error = 'please input name'
            return render_template('register.html', error=error)
        elif not request.form['email']:
            error = 'please input email'
            return render_template('register.html', error=error)
        elif not request.form['password']:
            error = 'please input password'
            return render_template('register.html', error=error)
        elif request.form['password'] != request.form['password2']:
            error = 'please check that you have entered it correctly'
            return render_template('register.html', error=error)
        elif student['StudentName'] != request.form['username']:
            error = 'Invalid your studentID and Name'
            return render_template('register.html', error=error)
        else:
            g.db.execute('''insert into User (StudentID, UserName, UserPassword, UserEmail) values (%s, %s, %s, %s)''', [id, name, password,email])
            return redirect(url_for('next_register'))

@app.route('/confirm_register')
def next_register():
    return render_template('confirm_register.html')

@app.route('/information')
def information():
    return render_template('information.html')

@app.route('/timetable_504')
def timetable_504():
    if not g.user:
        return redirect(url_for('login'))
    return render_template('timetable_504.html')

@app.route('/timetable_519')
def timetable_519():
    return render_template('timetable_519.html')

@app.route('/master_reservation')
def master_reservation():
    return render_template('master_reservation.html')

@app.route('/checkinformation')
def checkinformation():
    return render_template('checkinformation.html')

@app.route('/selectlist')
def selectlist():
    return render_template('selectlist.html')

@app.route('/finish')
def finish_reservation():
    return render_template('finish_reservation.html')

@app.route('/student_member')
def student_member():
    return render_template('student_member.html')

if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(debug=True)
