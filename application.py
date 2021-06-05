from flask import Flask, Blueprint, render_template, session, request, flash, url_for, redirect
from auth import auth
import requests
import json
import os

application = Flask(__name__)
application.config['SECRET_KEY'] = "\x07/\xc2\xbc\xfd\xb9\xb3<\x1f\xd40\xef3\x92\x01\xeb&\xbd\x8f\xe8r\xc3\xb6"
application.register_blueprint(auth)
ENDPOINT_API = "https://iw6n2bfzzd.execute-api.ap-southeast-2.amazonaws.com/prod/"

@application.route('/')
def root():
	print(os.urandom(24))
	return render_template('index.html')	
	
@application.route('/search')
def search():
	return render_template('search.html')
	
@application.route('/user/<username>')
def user_page(username):
	
	data = {'username': username}
	json_data = json.dumps(data)
	url = ENDPOINT_API + 'user'
	response = requests.get(url, data=json_data)
	response = json.loads(response.text)
	user = response['user']
	
	if not user:
		user = ''
	
	return render_template('user.html', user=user)

#Check username in session, return empty string if no username
def getUsername():
	username = ''
	if 'username' in session:
		username = session['username']
		
	return username

if __name__ == "__main__":
	application.debug = True
	application.run()
	