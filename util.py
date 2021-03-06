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
	
def getPetByPetId(pet_id):
	pet = ''
	
	data = {'id': pet_id}
	json_data = json.dumps(data)
	url = ENDPOINT_API + 'pet'
	response = requests.get(url, data=json_data)
	response = json.loads(response.text)
	
	if 'pet' in response:
		pet = response['pet']
		
	if pet == None:
		pet = ''
		
	return pet
	
def getRatingByRatingId(rating_id):
	rating = 0
	
	data = {'id': rating_id}
	json_data = json.dumps(data)
	url = ENDPOINT_API + 'rating'
	response = requests.get(url, data=json_data)
	response = json.loads(response.text)
	
	if 'rating' in response:
		rating = response['rating']
	
	return rating
	
def getCommentsByPetId(pet_id):
	comments = {}
	
	data = {'pet_id': pet_id}
	json_data = json.dumps(data)
	url = ENDPOINT_API + 'pet/comment'
	response = requests.get(url, data=json_data)
	response = json.loads(response.text)
	
	if 'comments' in response:
		comments = response['comments']
		
	return comments

def getAverageRatingByPetId(pet_id):
	average = 0
	
	data = {'pet_id': pet_id}
	json_data = json.dumps(data)
	url = ENDPOINT_API + 'pet/average-rating'
	response = requests.get(url, data=json_data)
	response = json.loads(response.text)
	
	if 'average_rating' in response:
		average = response['average_rating']
		
	return average
	
def getSearchResults(search):
	results = []
	
	data = {'search': search}
	json_data = json.dumps(data)
	url = ENDPOINT_API + 'search'
	response = requests.get(url, data=json_data)
	response = json.loads(response.text)
	
	if 'pets' in response:
		results = response['pets']
		
	return results

def getPetsByOwner(username):
	results = []
	
	data = {'username': username}
	json_data = json.dumps(data)
	url = ENDPOINT_API + 'user/pets'
	response = requests.get(url, data=json_data)
	response = json.loads(response.text)
	
	if 'pets' in response:
		results = response['pets']
		
	return results
	
def getPetsRatedByUser(username):
	results = []
	
	data = {'username': username}
	json_data = json.dumps(data)
	url = ENDPOINT_API + 'user/rated'
	response = requests.get(url, data=json_data)
	response = json.loads(response.text)
	
	if 'rated_pets' in response:
		results = response['rated_pets']
		
	return results
	
	
	