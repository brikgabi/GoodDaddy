
# hello world!!
from flask import Flask, render_template,json, request, redirect, url_for
# from flask.ext.mysql import MySQL
from flaskext.mysql import MySQL

CURRENT_USER = None
CURRENT_MATCH = None

class User(object):
    def __init__(self, first_name, last_name, startup_name, website, email):
        self.first_name = first_name
        self.last_name = last_name
        self.startup_name = startup_name
        self.website = website
        self.email = email

    
app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Test!234'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route("/home")
@app.route("/home/<user>")
def home():
    if CURRENT_USER == None:
        return render_template('index.html')
    else:
        return render_template('index.html', user = CURRENT_USER.first_name)


@app.route("/")
def main():
    return render_template('index.html')

@app.route("/showSignUp")
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp', methods=['POST'])
def signUp():
    #wassuupppp

    _first_name = request.form['inputFName']
    _last_name = request.form['inputLName']
    _startup = request.form['inputStartup']
    _website = request.form['inputWebsite']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']


    if _first_name and _last_name and _startup and _email and _password:
        global CURRENT_USER, CURRENT_MATCH
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('sp_addUsers',(_first_name, _last_name, _startup, _website, _email, _password))

        cursor.execute('SELECT first_name, last_name, startup_name, website from `tbl_USERS` WHERE email="%s" AND password="%s";' %(_email, _password))
        row = cursor.fetchone()
        row_count = cursor.rowcount

        if row_count == 1:
            first_name = row[0].encode('ascii', 'ignore')
            last_name = row[1].encode('ascii', 'ignore')
            startup_name = row[2].encode('ascii', 'ignore')
            website = row[3].encode('ascii', 'ignore')
            CURRENT_USER = User(first_name, last_name, startup_name, website, _email)

            cursor.execute('SELECT first_name, last_name, startup_name, website, email from `tbl_USERS` WHERE email<>"%s";' %_email)
            row2 = cursor.fetchone()
            first_name = row2[0].encode('ascii', 'ignore')
            last_name = row2[1].encode('ascii', 'ignore')
            startup_name = row2[2].encode('ascii', 'ignore')
            website = row2[3].encode('ascii', 'ignore')
            email2 = row2[4].encode('ascii', 'ignore')
            CURRENT_MATCH = User(first_name, last_name, startup_name, website, email2)

        data = cursor.fetchall()

        if len(data) is 0:
            conn.commit()
            return json.dumps({'message':'User created successfully !'})
        else:
            return json.dumps({'error':str(data[0])})
    else:
        return json.dumps({'html':'<span>Enter the required fields</span>'})

@app.route('/showSignIn')
def showSignIn():
    return render_template('signin.html')

@app.route('/rand-uhm')
def randomMatch():
    global CURRENT_MATCH
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT first_name, last_name, startup_name, website, email from `tbl_USERS` WHERE email<>"%s" ORDER BY RAND() LIMIT 1;' %CURRENT_USER.email)
    row2 = cursor.fetchone()
    first_name = row2[0].encode('ascii', 'ignore')
    last_name = row2[1].encode('ascii', 'ignore')
    startup_name = row2[2].encode('ascii', 'ignore')
    website = row2[3].encode('ascii', 'ignore')
    email2 = row2[4].encode('ascii', 'ignore')
    CURRENT_MATCH = User(first_name, last_name, startup_name, website, email2)
    return render_template('profile.html', user=CURRENT_USER.first_name, matchFName=CURRENT_MATCH.first_name,
                    matchLName=CURRENT_MATCH.last_name, matchWebsite=CURRENT_MATCH.website,
                    matchEmail= CURRENT_MATCH.email, matchStartup= CURRENT_MATCH.startup_name)


@app.route('/signIn', methods=['POST'])
def signIn():
    global CURRENT_USER, CURRENT_MATCH
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    if _email and _password:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT first_name, last_name, startup_name, website from `tbl_USERS` WHERE email="%s" AND password="%s";' %(_email, _password))
        row = cursor.fetchone()
        row_count = cursor.rowcount
        if row_count == 1:
            first_name = row[0].encode('ascii', 'ignore')
            last_name = row[1].encode('ascii', 'ignore')
            startup_name = row[2].encode('ascii', 'ignore')
            website = row[3].encode('ascii', 'ignore')
            CURRENT_USER = User(first_name, last_name, startup_name, website, _email)
            row_count = cursor.rowcount

            cursor.execute('SELECT first_name, last_name, startup_name, website, email from `tbl_USERS` WHERE email<>"%s" ORDER BY RAND() LIMIT 1;' %_email)
            row2 = cursor.fetchone()
            first_name = row2[0].encode('ascii', 'ignore')
            last_name = row2[1].encode('ascii', 'ignore')
            startup_name = row2[2].encode('ascii', 'ignore')
            website = row2[3].encode('ascii', 'ignore')
            email2 = row2[4].encode('ascii', 'ignore')
            CURRENT_MATCH = User(first_name, last_name, startup_name, website, email2)
        if row_count == 1:
            return json.dumps({'message': 'ok worked'})
        else:
            return json.dumps({'message':'uhhh either 0 or more than one account like this'})


@app.route('/profile')
@app.route('/profile/<user>')
def showProfile():
    if CURRENT_USER != None:
        return render_template('profile.html', user=CURRENT_USER.first_name, matchFName=CURRENT_MATCH.first_name,
                                matchLName=CURRENT_MATCH.last_name, matchWebsite=CURRENT_MATCH.website,
                               matchEmail= CURRENT_MATCH.email, matchStartup= CURRENT_MATCH.startup_name)
    else:
        return render_template('profile.html')



if __name__ == "__main__":
    app.run()
