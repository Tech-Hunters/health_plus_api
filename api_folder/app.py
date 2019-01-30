import json
from flask import Flask, jsonify
import mysql.connector
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	passwd="",
	database="health_plus"
	)

@app.route('/get-user', methods=['GET'])
def get_user():
	mycursor = mydb.cursor()
    mycursor.execute("select * from user")
    return jsonify({'tasks': [i[0] for i in mycursor.fetchall()]})


class User(Resource):
	def get(self):
		mycursor = mydb.cursor()
		mycursor.execute("select * from user") # This line performs query and returns json result
	return {'user': [i[0] for i in mycursor.fetchall()]} # Fetches first column that is Employee ID

class Doctor(Resource):
	def get(self):
		mycursor = mydb.cursor()
		mycursor.execute("select * from doctor") # This line performs query and returns json result
	return {'doctor': [i[0] for i in mycursor.fetchall()]} # Fetches first column that is Employee ID

class Hospital(Resource):
	def get(self):
		mycursor = mydb.cursor()
		mycursor.execute("select * from hospital") # This line performs query and returns json result
	return {'doctor': [i[0] for i in mycursor.fetchall()]} # Fetches first column that is Employee ID

api.add_resource(User, '/user')
api.add_resource(Doctor, '/doctor')
api.add_resource(Hospital, '/hospital')


@app.route('/')
def index():
	return "wow"

	if __name__ == '__main__':
		app.run(port='8000')