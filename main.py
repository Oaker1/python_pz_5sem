import json
from flask import Flask, jsonify, request
import psycopg2 # MACOSX: psycopg2-binary
import random
app = Flask(__name__)
data = "Hello world"

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="test"
)
cursor = conn.cursor()

success_message = {'success': True}

@app.route("/")
def homepage():
    return data

@app.route('/users', methods=['GET'])
def get_users():
    sql = 'SELECT * FROM phonenames;'
    cursor.execute(sql)
    data = cursor.fetchall()
    return data


@app.route('/users/<userid>', methods=['GET'])
def get_user(userid):
    sql = 'SELECT * FROM phonenames WHERE uid = %s'
    cursor.execute(sql, (str(userid),) )
    data = cursor.fetchall()
    print(data)
    return jsonify(data)


@app.route('/users', methods=['POST'])
def add_user():
    sql = 'INSERT INTO phonenames VALUES (%s, %s, %s ,%s)'
    uid = random.randint(0, 999)
    name = request.json['name']
    street = request.json['street']
    phone = request.json['phone']
    cursor.execute(sql, (uid, name, street, phone))
    conn.commit()
    return get_user(uid)


@app.route('/users', methods=['DELETE'])
def del_all():
    sql = 'TRUNCATE phonenames'
    cursor.execute(sql)
    conn.commit()
    return data


@app.route('/users/<userid>', methods=['DELETE'])
def del_user(userid):
    sql = 'DELETE FROM phonenames WHERE uid = %s'
    cursor.execute(sql, (str(userid),) )
    conn.commit()
    return data


@app.route('/users/<userid>', methods=['PUT'])
def update_user(userid):
    uid = userid
    name = request.json['name']
    street = request.json['street']
    phone = request.json['phone']
    sql = 'UPDATE phonenames SET name = %s, street = %s,  phone = %s WHERE uid = %s;'
    cursor.execute(sql, ((name, street, phone, uid)))
    conn.commit()
    return data


if __name__ == '__main__':
    app.run(debug=True)
