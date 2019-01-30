from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import time, datetime
import jwt
from functools import wraps
import sqlalchemy_jsonfield

current_milli_time = lambda: int(round(time.time() * 1000))
app = Flask(__name__)
app.config['SECRET_KEY'] = "secretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:3071Thet@localhost:3306/health_plus'

db = SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50))
    user_password = db.Column(db.String(255))
    user_email = db.Column(db.String(50))
    user_phno = db.Column(db.String(50))
    user_image = db.Column(db.String(255))
    login_type = db.Column(db.String(50))

class HealthTip(db.Model):
    ht_id = db.Column(db.Integer, primary_key=True)
    ht_title = db.Column(db.String(255))
    ht_details = db.Column(db.Text())
    ht_image = db.Column(db.String(255))
    ht_time = db.Column(db.DateTime(timezone=True))


class Doctor(db.Model):
    doctor_id = db.Column(db.Integer, primary_key=True)
    doctor_name = db.Column(db.String(50))
    doctor_edu = db.Column(db.String(50))
    doctor_image = db.Column(db.String(255))
    doctor_category = db.Column(db.String(50))


class Hospital(db.Model):
    hospital_id = db.Column(db.Integer, primary_key=True)
    hospital_name = db.Column(db.String(255))
    hospital_address = db.Column(db.String(255))
    hospital_phno = db.Column(db.String(50))
    hospital_image = db.Column(db.String(255))
    hospital_location = db.Column(sqlalchemy_jsonfield.JSONField())

class Schedule(db.Model):
    schedule_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date())
    time = db.Column(db.Time())
    note = db.Column(db.Text())

def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = None

		if 'x-access-token' in request.headers:
			token = request.headers['x-access-token']
		if not token:
			return jsonify({'message' : 'Token is missing'})

		try:
			data = jwt.decode(token, app.config['SECRET_KEY'])
			current_user = User.query.filter_by(user_id=data['user_id']).first()
		except:
			return jsonify({'message' : 'Token is invalid'}), 401

		return f(current_user, *args, **kwargs)
	return decorated

@app.route('/login')
def login():
	auth = request.authorization
	if not auth or not auth.username or not auth.password:
		return make_response("Could not verify", 401, {'WWW-Authenticate': 'Basic releam="login Required!"'})
	user = User.query.filter_by(user_name=auth.username).first()

	if not user:
		return make_response("Could not verify", 401, {'WWW-Authenticate': 'Basic releam="login Required!"'})

	if check_password_hash(user.user_password, auth.password):
		token = jwt.encode({'user_id': user.user_id, 'exp': datetime.datetime.utcnow()+datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
		return jsonify({'token': token.decode('UTF-8')})

	return make_response("Could not verify", 401, {'WWW-Authenticate': 'Basic releam="login Required!"'})



@app.route('/user', methods=['GET'])
def get_all_users():
	
	users = User.query.all()
	output = []

	for user in users:
		user_data = {}
		user_data['id'] = user.user_id
		user_data['name'] = user.user_name
		user_data['email'] = user.user_email
		user_data['phno'] = user.user_phno
		user_data['image'] = user.user_image
		user_data['login_type'] = user.login_type
		output.append(user_data)

	return jsonify({'users': output})

@app.route('/user/<user_id>', methods=['GET'])
def get_one_user(user_id):
	user = User.query.filter_by(user_id = user_id).first()
	if not user:
		return jsonify({ 'message': 'User not found'})

	user_data = {}
	user_data['id'] = user.user_id
	user_data['name'] = user.user_name
	user_data['email'] = user.user_email
	user_data['phno'] = user.user_phno
	user_data['image'] = user.user_image
	user_data['login_type'] = user.login_type
	return jsonify({'user': user_data})

@app.route('/user', methods=['POST'])
def create_user():
	data = request.get_json()
	hashed_password = generate_password_hash(data['password'], method='md5')
	new_user = User(user_id=str(current_milli_time()), 
		user_name=data['name'], 
		user_password=hashed_password, 
		user_image=data['image'],
		user_email=data['email'],
		user_phno=data['phno'],
		login_type=data['login_type'])

	db.session.add(new_user)
	db.session.commit()

	return jsonify({'message': 'New User Created'})

@app.route('/user', methods=['PUT'])
def update_user():
	data = request.get_json()
	user = User.query.filter_by(user_id = data['user_id']).first()
	if not user:
		return jsonify({ 'message': 'User not found'})

	for col in data:
		if col=="name":
			user.user_name = data[col]
		elif col=="image":
			user.user_image = data[col]
		elif col=="email":
			user.user_email = data[col]
		elif col=="phno":
			user.user_phno = data[col]
	db.session.commit()

	return jsonify({'message': 'User has been updated'})

@app.route('/user/<user_id>', methods=['DELETE'])
@token_required
def delete_user(current_user,user_id):
	user = User.query.filter_by(user_id = user_id).first()
	if not user:
		return jsonify({ 'message': 'User not found'})

	db.session.delete()
	db.session.commit()
	return jsonify({'message': 'User has been deleted successfully'})

@app.route('/health_tip', methods=['GET'])
def get_all_healthtips():
	
	health_tips = HealthTip.query.all()
	output = []

	for health_tip in health_tips:
		health_tip_data = {}
		health_tip_data['ht_id'] = health_tip.ht_id
		health_tip_data['ht_title'] = health_tip.ht_title
		health_tip_data['ht_details'] = health_tip.ht_details
		health_tip_data['ht_image'] = health_tip.ht_image
		health_tip_data['ht_time'] = health_tip.ht_time
		output.append(health_tip_data)

	return jsonify({'health_tips': output})

@app.route('/health_tip/<ht_id>', methods=['GET'])
def get_one_health_tip(ht_id):
	health_tip = HealthTip.query.filter_by(ht_id = ht_id).first()
	if not health_tip:
		return jsonify({ 'message': 'Health tip not found'})

	health_tip_data = {}
	health_tip_data['ht_id'] = health_tip.ht_id
	health_tip_data['ht_title'] = health_tip.ht_title
	health_tip_data['ht_details'] = health_tip.ht_details
	health_tip_data['ht_image'] = health_tip.ht_image
	health_tip_data['ht_time'] = health_tip.ht_time
	return jsonify({'health_tip': health_tip_data})

@app.route('/health_tip', methods=['POST'])
def create_health_tip():
	data = request.get_json()
	new_health_tip = HealthTip(ht_id=str(current_milli_time()), 
		ht_title=data['ht_title'], 
		ht_details=data['ht_details'], 
		ht_image=data['ht_image'],
		ht_time=datetime.datetime.now())

	db.session.add(new_health_tip)
	db.session.commit()

	return jsonify({'message': 'New health tip has been Created'})

@app.route('/health_tip', methods=['PUT'])
def update_health_tip():
	data = request.get_json()
	health_tip = HealthTip.query.filter_by(health_tip_id = data['id']).first()
	if not health_tip:
		return jsonify({ 'message': 'Health Tip not found'})

	for col in data:
		if col=="ht_title":
			health_tip.ht_title = data[col]
		elif col=="ht_details":
			health_tip.ht_details = data[col]
		elif col=="ht_image":
			health_tip.ht_email = data[col]
		elif col=="ht_time":
			health_tip.ht_time = data[col]
	db.session.commit()

	return jsonify({'message': 'HealthTip has been updated'})

@app.route('/health_tip/<ht_id>', methods=['DELETE'])
@token_required
def delete_health_tip(current_user,ht_id):
	health_tip = HealthTip.query.filter_by(ht_id = ht_id).first()
	if not health_tip:
		return jsonify({ 'message': 'Health tip not found'})

	db.session.delete(health_tip)
	db.session.commit()
	return jsonify({'message': 'health tip has been deleted successfully'})


@app.route('/doctor', methods=['GET'])
def get_all_doctors():
	
	doctors = Doctor.query.all()
	output = []

	for doctor in doctors:
		doctor_data = {}
		doctor_data['id'] = doctor.doctor_id
		doctor_data['name'] = doctor.doctor_name
		doctor_data['edu'] = doctor.doctor_edu
		doctor_data['image'] = doctor.doctor_image
		doctor_data['category'] = doctor.doctor_category
		output.append(doctor_data)

	return jsonify({'doctors': output})

@app.route('/doctor/<doctor_id>', methods=['GET'])
def get_one_doctor(doctor_id):
	doctor = Doctor.query.filter_by(doctor_id = doctor_id).first()
	if not doctor:
		return jsonify({ 'message': 'Doctor not found'})

	doctor_data = {}
	doctor_data['id'] = doctor.doctor_id
	doctor_data['name'] = doctor.doctor_name
	doctor_data['edu'] = doctor.doctor_edu
	doctor_data['image'] = doctor.doctor_image
	doctor_data['category'] = doctor.doctor_category
	return jsonify({'doctor': doctor_data})

@app.route('/doctor', methods=['POST'])
def create_doctor():
	data = request.get_json()
	new_doctor = Doctor(doctor_id=str(current_milli_time()), 
		doctor_name=data['name'], 
		doctor_edu=data['edu'], 
		doctor_image=data['image'],
		doctor_category=data['category'])

	db.session.add(new_doctor)
	db.session.commit()

	return jsonify({'message': 'New Doctor Created'})

@app.route('/doctor', methods=['PUT'])
def update_doctor():
	return ''

@app.route('/doctor/<doctor_id>', methods=['DELETE'])
@token_required
def delete_doctor(current_user,doctor_id):
	doctor = Doctor.query.filter_by(doctor_id = doctor_id).first()
	if not doctor:
		return jsonify({ 'message': 'Doctor not found'})

	db.session.delete(doctor)
	db.session.commit()
	return jsonify({'message': 'doctor has been deleted successfully'})


@app.route('/hospital', methods=['GET'])
def get_all_hospitals():
	
	hospitals = Hospital.query.all()
	output = []

	for hospital in hospitals:
		hospital_data = {}
		hospital_data['id'] = hospital.hospital_id
		hospital_data['name'] = hospital.hospital_name
		hospital_data['address'] = hospital.hospital_address
		hospital_data['phno'] = hospital.hospital_phno
		hospital_data['image'] = hospital.hospital_image
		hospital_data['location'] = hospital.hospital_location
		output.append(hospital_data)

	return jsonify({'hospitals': output})

@app.route('/hospital/<hospital_id>', methods=['GET'])
def get_one_hospital(hospital_id):
	hospital = Hospital.query.filter_by(hospital_id = hospital_id).first()
	if not hospital:
		return jsonify({ 'message': 'Hospital not found'})

	hospital_data = {}
	hospital_data['id'] = hospital.hospital_id
	hospital_data['name'] = hospital.hospital_name
	hospital_data['address'] = hospital.hospital_address
	hospital_data['phno'] = hospital.hospital_phno
	hospital_data['image'] = hospital.hospital_image
	hospital_data['location'] = hospital.hospital_location
	return jsonify({'hospital': hospital_data})

@app.route('/hospital', methods=['POST'])
def create_hospital():
	data = request.get_json()
	new_hospital = Hospital(hospital_id=str(current_milli_time()), 
		hospital_name=data['name'], 
		hospital_address=data['address'],
		hospital_phno=data['phno'],
		hospital_image=data['image'],
		hospital_location=data['location'],)

	db.session.add(new_hospital)
	db.session.commit()

	return jsonify({'message': 'New Hospital Created'})

@app.route('/hospital', methods=['PUT'])
def update_hospital():
	return ''

@app.route('/hospital/<hospital_id>', methods=['DELETE'])
@token_required
def delete_hospital(current_user,hospital_id):
	doctor = Hospital.query.filter_by(hospital_id = hospital_id).first()
	if not doctor:
		return jsonify({ 'message': 'Hospital not found'})

	db.session.delete(hospital)
	db.session.commit()
	return jsonify({'message': 'hospital has been deleted successfully'})


@app.route('/schedule', methods=['GET'])
def get_all_schedule():
	
	schedules = Schedule.query.all()
	output = []

	for schedule in schedules:
		schedule_data = {}
		schedule_data['id'] = schedule.schedule_id
		schedule_data['user_id'] = schedule.user_id
		schedule_data['note'] = schedule.note
		schedule_data['date'] = schedule.date
		schedule_data['time'] = str(schedule.time)
		output.append(schedule_data)

	return jsonify({'schedules': output})

@app.route('/schedule/user/<user_id>', methods=['GET'])
def get_schedule_by_user_id(user_id):
	schedules = Schedule.query.filter_by(user_id = user_id)
	if not schedules:
		return jsonify({ 'message': 'Schedule not found'})

	output = []

	for schedule in schedules:
		schedule_data = {}
		schedule_data['id'] = schedule.schedule_id
		schedule_data['user_id'] = schedule.user_id
		schedule_data['note'] = schedule.note
		schedule_data['date'] = schedule.date
		schedule_data['time'] = str(schedule.time)
		output.append(schedule_data)

	return jsonify({'schedules': output})

@app.route('/schedule/<schedule_id>', methods=['GET'])
def get_one_schedule(schedule_id):
	schedule = Schedule.query.filter_by(schedule_id = schedule_id).first()
	if not schedule:
		return jsonify({ 'message': 'Schedule not found'})

	schedule_data = {}
	schedule_data['id'] = schedule.schedule_id
	schedule_data['user_id'] = schedule.user_id
	schedule_data['note'] = schedule.note
	schedule_data['date'] = schedule.date
	schedule_data['time'] = str(schedule.time)
	return jsonify({'schedule': schedule_data})

@app.route('/schedule', methods=['POST'])
def create_schedule():
	data = request.get_json()
	new_schedule = Hospital(schedule_id=str(current_milli_time()), 
		user_id=data['user_id'], 
		date=data['date'],
		time=data['time'],
		note=data['note'],)

	db.session.add(new_schedule)
	db.session.commit()

	return jsonify({'message': 'New Schedule Created'})

@app.route('/hospital', methods=['PUT'])
def update_schedule():
	return ''

@app.route('/hospital/<schedule_id>', methods=['DELETE'])
def delete_schedule(schedule_id):
	schedule = Schedule.query.filter_by(schedule_id = schedule_id).first()
	if not schedule:
		return jsonify({ 'message': 'Schedule not found'})

	db.session.delete(schedule)
	db.session.commit()
	return jsonify({'message': 'schedule has been deleted successfully'})

if __name__ == "__main__":
    app.run(debug=True)
