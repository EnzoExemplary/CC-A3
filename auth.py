from flask import Flask, Blueprint, render_template, session, redirect, url_for, request, flash
import requests
import json

auth = Blueprint('auth', __name__, template_folder='templates')
ENDPOINT_API = "https://iw6n2bfzzd.execute-api.ap-southeast-2.amazonaws.com/prod/"

@auth.route('/login')
def login():
	return render_template('login.html')
	
@auth.route('/login', methods=['POST'])
def login_post():
	username = request.form.get('username')
	password = request.form.get('password')
	
	data = {'username': username, 'password': password}
	json_data = json.dumps(data)
	url = ENDPOINT_API + 'login'
	response = requests.post(url, data=json_data)
	response = json.loads(response.text)
	
	if(response['match']):
		session['username'] = username
		redirect_url = '/user/' + username
		return redirect(redirect_url)
	else:
		flash('Username or password is invalid')
		return redirect(url_for('auth.login'))
	
#Check username in session, return empty string if no username
def getUsername():
	username = ''
	if 'username' in session:
		username = session['username']
		
	return username	

@auth.route('/register')
def register():
	return render_template('register.html')