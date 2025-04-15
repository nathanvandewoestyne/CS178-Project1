import pymysql
import creds
from flask import Flask
from flask import render_template
from flask import Flask, render_template, request, redirect, url_for, flash



# establish connection used ChatGPT
conn = pymysql.connect(
    host=creds.host,
    user=creds.user,
    password=creds.password,
    db=creds.db,
    port=creds.port,
    cursorclass=pymysql.cursors.DictCursor
)

app = Flask(__name__)
app.secret_key = 'your_secret_key' # this is an artifact for using flash displays; 
                                   # it is required, but you can leave this alone
@app.route('/')
def home():
    return render_template('home.html')


# example usage (inside a route)
@app.route('/users')
def users():
    with conn.cursor() as cursor:
        cursor.execute("SELECT Name FROM country WHERE Name LIKE 'U%'")
        results = cursor.fetchall()
    return render_template('users.html', users=results)





# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

#Ask chatgpt about collisoditing python installations
