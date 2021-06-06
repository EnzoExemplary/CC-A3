from flask import Flask, session
import requests
import json

ENDPOINT_API = "https://iw6n2bfzzd.execute-api.ap-southeast-2.amazonaws.com/prod/"

#Check username in session, return empty string if no username
def getUsername():
	username = ''
	if 'username' in session:
		username = session['username']
		
	return username
	
def getUserByUsername(username):
	user = ''
	
	data = {'username': username}
	json_data = json.dumps(data)
	url = ENDPOINT_API + 'user'
	response = requests.get(url, data=json_data)
	response = json.loads(response.text)
	
	if 'user' in response:
		user = response['user']
	
	return user