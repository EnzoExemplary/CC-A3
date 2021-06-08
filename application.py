from flask import Flask, Blueprint, render_template, session, request, flash, url_for, redirect
from auth import auth
from util import getUsername, getUserByUsername, getPetByPetId, getRatingByRatingId
import requests
import json
import base64
from base64 import b64encode


application = Flask(__name__)
application.config['SECRET_KEY'] = "\x07/\xc2\xbc\xfd\xb9\xb3<\x1f\xd40\xef3\x92\x01\xeb&\xbd\x8f\xe8r\xc3\xb6"
application.register_blueprint(auth)
ENDPOINT_API = "https://iw6n2bfzzd.execute-api.ap-southeast-2.amazonaws.com/prod/"

@application.route('/')
def root():
	user = getUserByUsername(getUsername())
	return render_template('index.html', user=user)	
	
@application.route('/search')
def search():
	user = getUserByUsername(getUsername())
	return render_template('search.html', user=user)
	
@application.route('/user/<username>')
def user_page(username):
	return render_template('user.html', user=getUserByUsername(username))
	
@application.route('/pet/<pet_id>')
def pet_page(pet_id):
	username = getUsername()
	user = getUserByUsername(username)
	pet = getPetByPetId(pet_id) 
	rating = getRatingByRatingId(pet_id + username)
	
	return render_template('pet.html', user = user, pet = pet, rating = rating)

@application.route('/add_pet')
def add_pet():
	user = getUserByUsername(getUsername())
	return render_template('add_pet.html', user=user)	

@application.route('/add_pet', methods=['POST'])
def add_pet_post():
	user = getUserByUsername(session['username'])
	image = request.files.get('img')
	pet_name = request.form.get('name')
	image_bytes = base64.b64encode(image.read())
	image_string = image_bytes.decode('utf-8')
	folder_name = 'pet_images'
	
	data = {
		'pet_name': pet_name,
		'folder_name': folder_name,
		'image': image_string, 
		'username': user['username'], 
		'num_pets': user['num_pets']
	}
	json_data = json.dumps(data)
	url = ENDPOINT_API + 'add-pet'
	response = requests.post(url, data=json_data)
	response = json.loads(response.text)
	
	if response['success']:
		flash('Pet uploaded successfully!')
	else:
		flash('Upload failed...')
		
	return redirect(url_for('add_pet'))
	
@application.route('/update_rating', methods=['POST'])
def update_rating():
	rating_details = request.get_json()
	api_url = ENDPOINT_API + 'rating'
	json_data = json.dumps(rating_details)
	response = requests.post(api_url, data=json_data)
	
	return json_data

if __name__ == "__main__":
	application.debug = True
	application.run()
	