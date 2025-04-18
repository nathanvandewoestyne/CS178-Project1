

import pymysql
import creds




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



