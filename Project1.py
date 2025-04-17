import pymysql
import creds
from flask import Flask
from flask import render_template
from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session


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
                                   
@app.route('/', methods=['GET', 'POST'])
def search_city_language():
    languages = []
    city = ''
    if request.method == 'POST':
        city = request.form['city']
        with conn.cursor() as cursor:
            sql = """
                SELECT cl.language
                FROM city c
                JOIN country co ON c.countrycode = co.code
                JOIN countrylanguage cl ON co.code = cl.countrycode
                WHERE LOWER(c.name) = LOWER(%s);
            """
            cursor.execute(sql, (city,))
            languages = cursor.fetchall()
    return render_template('search.html', city=city, languages=languages)

if __name__ == '__main__':
    app.run(debug=True)
# example usage (inside a route)
@app.route('/users')
def users():
    with conn.cursor() as cursor:
        cursor.execute("SELECT Name FROM country WHERE Name LIKE 'U%'")
        results = cursor.fetchall()
    return render_template('users.html', users=results)

#Keep track of user
app.route('/log-in-user', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        session['username'] = name

app.route('/display-user-status')
def user_stats():
    key = {"Name":session['username']}
    response = table.get_item(Key=key)


# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

#Ask chatgpt about collisoditing python installations
