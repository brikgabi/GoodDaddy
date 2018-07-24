
# hello world!!
from flask import Flask, render_template,json, request, redirect, url_for
# from flask.ext.mysql import MySQL
from flaskext.mysql import MySQL



app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Test!234'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/showSignUp")
def showSignUp():
    return render_template('signup.html')


@app.route('/signUp', methods=['POST'])
def signUp():
    #wassuupppp

    _name = request.form['inputName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    if _name and _email and _password:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('sp_createUser',(_name,_email,_password))

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

@app.route('/signIn', methods=['POST'])
def signIn():
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    if _email and _password:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * from `tbl_user` WHERE user_username="%s" AND user_password="%s";' %(_email, _password))
        row_count = cursor.rowcount
        if row_count == 1:
            return json.dumps({'message': 'ok worked'})
        else:
            return json.dumps({'message':'uhhh either 0 or more than one account like this'})

@app.route('/profile')
def showProfile():
    return render_template('profile.html')



if __name__ == "__main__":
    app.run()
