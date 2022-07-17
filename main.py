import os
#import requests
import flask
from flask import request,abort
import psycopg2
from datetime import datetime

app = flask.Flask(__name__)

db_conn = None
db_cursor = None
#ip_header_name = 'X-Forwarded-For'
ip_header_name = 'Host'

@app.route('/', methods=['GET'])
def do_work():
    select_addr = "select * from blacklist where ip_addr = %s limit 1"
    ip_addr = request.headers[ip_header_name]
    db_cursor.execute(select_addr, (ip_addr,))
    if db_cursor.rowcount > 0:
        abort(404)
    args = request.args
    n = args.get('n', type=int)
    if n:
        return format(n*n, 'd') + '\n'
    return 'Param error', 400

@app.route('/blacklisted', methods=['GET'])
def blacklist():
    insert_addr = "insert into blacklist (ip_addr, path, time) values (%s,%s,%s);"
    ip_addr = request.headers[ip_header_name]
    tstamp = datetime.now()
    print (db_cursor.mogrify(insert_addr, (ip_addr,"/blacklisted",tstamp)))
    db_cursor.execute(insert_addr, (ip_addr,"/blacklist",tstamp))
    db_conn.commit()
    abort(404)


if __name__ == '__main__':
    db_host = os.environ.get("DB_HOST")
    db_name = os.environ.get("DB_NAME")
    db_user = os.environ.get("DB_USER")
    db_pass = os.environ.get("DB_PASS")
    db_conn = psycopg2.connect(host=db_host,
                               database=db_name,
                               user=db_user,
                               password=db_pass)
    db_cursor = db_conn.cursor()
    app.run(host='0.0.0.0',port=8080)