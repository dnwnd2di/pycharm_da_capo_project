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
    print (g.db)

    data = g.db.fetchall()
    print data
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

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/check_login',  methods=["POST"])
def login_check():
    if request.method == "POST":
        id = request.form['id']
        password = request.form['password']

        user = query_db('''select * from User where StudentID = %s''', [id], one=True)
        print user
        if password == user['UserPassword']:
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
        print(password)
        email = request.form['email']
        g.db.execute('''insert into User (StudentID, UserName, UserPassword, UserEmail) values (%s, %s, %s, %s)''', [id, name, password,email])
        return redirect(url_for('confirm_register'))

@app.route('/confirm_register')
def next_register():
    return render_template('confirm_register.html')

@app.route('/information')
def information():
    return render_template('information.html')

@app.route('/timetable_504')
def timetable():
    return render_template('timetable_504.html')



if __name__ == "__main__":
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run(debug=True)
