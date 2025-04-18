import pymysql
import creds
import uuid
from flask import Flask
from flask import render_template
from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session
import boto3
#import DbCode


##Code from DbCode
def get_languages_by_city(city):
    sql = """
      SELECT cl.language, cl.isofficial, cl.percentage
      FROM city ci
      JOIN country c  ON ci.countrycode = c.code
      JOIN countrylanguage cl ON cl.countrycode = c.code
      WHERE ci.name = %s
    """
    with get_conn().cursor() as cur:
        cur.execute(sql, (city,))
        return cur.fetchall()


def get_user(username: str):
    resp = table.get_item(Key={'username': username})
    return resp.get('Item')





session = boto3.Session()

dynamo = session.resource('dynamodb')
table = dynamo.Table('Users')

conn = pymysql.connect(
    host=creds.host,
    user=creds.user,
    password=creds.password,
    db=creds.db,
    port=creds.port,
    cursorclass=pymysql.cursors.DictCursor
)

def get_log(log_id):
    resp = table.get_item(Key={'log_id': log_id})
    return resp.get('Item')

def get_all_logs():
    resp = table.scan()
    return resp.get('Items', [])



################################








app = Flask(__name__)
app.secret_key = "IdSTGBY2K4YuUcPS23EAg272OYyoHl9eydYFeZbW" # this is an artifact for using flash displays; 
                                   # it is required, but you can leave this alone


#ChatGPT
@app.route('/', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        # 1) pull form data:
        username = request.form['username']
        password = request.form['password']
        # 2) write it to your database…
        table.put_item(Item={'username': username, 'password': password})
        # 3) THEN redirect to your search view:
        return redirect(url_for('search_city_language'))
    # if GET (or after redirect) just show the form
    return render_template('register.html')



@app.route('/search', methods=['GET', 'POST'])
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


@app.route('/languages', methods=['GET','POST'])
def languages():
    city = request.form.get('city','').strip()
    langs = get_languages_by_city(city) if city else None
    return render_template('languages.html', city=city, languages=langs)



#Keep track of user

#ChatGPT
app.route('/log-in-user', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        session['username'] = name
    return


#Read
@app.route('/logs')
def logs():
    logs = get_all_logs()
    return render_template('logs.html', logs=logs)


@app.route('/crud')
def crud():
    return render_template('crud.html')




# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

#Ask chatgpt about collisoditing python installations
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

#Ask chatgpt about collisoditing python installations
