from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app,'friendsdb')
@app.route('/')
def index():
    query = "SELECT * FROM friends"
    friends = mysql.query_db(query)
    return render_template('index.html', all_friends=friends)
@app.route('/friends', methods=['POST'])
def create():
    query = "INSERT INTO friends (first_name, last_name, created_at, updated_at) VALUES (:first_name, :last_name, NOW(), NOW())"
    data = {
             'first_name': request.form['first_name'], 
             'last_name':  request.form['last_name'],
           }
    mysql.query_db(query, data)
    return redirect('/')
@app.route('/friends/<id>', methods=['POST'])
def update(id):
    data = {
             'first_name': request.form['first_name'], 
             'last_name':  request.form['last_name'],
             'id': id
           }
    query = "UPDATE friends SET first_name = :first_name, last_name = :last_name WHERE id = :id"
    mysql.query_db(query, data)
    return redirect('/')
@app.route('/friends/<id>/edit', methods=['GET'])
def edit(id):
    query = "SELECT * FROM friends WHERE id = :id"
    data = {
    'id': id
    }
    curr_friend = mysql.query_db(query, data)[0]
    print curr_friend
    return render_template('friends.html', id=id, curr_friend=curr_friend)
@app.route('/friends/<id>/delete', methods=['POST'])
def destroy(id):
    query = "DELETE FROM friends WHERE id = :id"
    data = {'id': id}
    mysql.query_db(query, data)
    return redirect('/')
app.run(debug=True)