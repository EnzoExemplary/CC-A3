from flask import Flask, Blueprint, render_template, session, redirect, url_for, request, flash
from auth import auth
from util import getAverageRatingByPetId
import requests
import json
import base64
from base64 import b64encode

api = Blueprint('api', __name__, template_folder='templates')
ENDPOINT_API = "https://iw6n2bfzzd.execute-api.ap-southeast-2.amazonaws.com/prod/"


def getLoginToken():
    token = request.headers['x-auth-token']
    return token


def getUsernameForToken(token):
    return token  # The token is just the username right now


def getUser(username):
    json_data = json.dumps({'username': username})
    url = ENDPOINT_API + 'user'
    response = requests.get(url, data=json_data)
    json_data = json.loads(response.text)

    return json_data


def getUserPets(username):
    json_data = json.dumps({'username': username})
    url = ENDPOINT_API + 'user/pets'
    response = requests.get(url, data=json_data)
    json_data = json.loads(response.text)
    if 'pets' in json_data:
        json_data = json_data['pets']
    return json_data


def getRatedUserPets(username):
    json_data = json.dumps({'username': username})
    url = ENDPOINT_API + 'user/rated'
    response = requests.get(url, data=json_data)
    json_data = json.loads(response.text)
    if 'rated_pets' in json_data:
        json_data = json_data['rated_pets']
    return json_data


def getPet(pet_id):
    json_data = json.dumps({
        'id': pet_id
    })
    url = ENDPOINT_API + 'pet'
    response = requests.get(url, data=json_data)
    json_data = json.loads(response.text)

    if 'pet' in json_data:
        json_data = json_data['pet']
        json_data['average'] = getAverageRatingByPetId(pet_id)
        json_data['comments'] = getPetComments(pet_id)

    return json_data


def getRandomPet():
    url = ENDPOINT_API + 'pet/random'
    response = requests.get(url)
    json_data = json.loads(response.text)

    if 'pet' in json_data:
        json_data = json_data['pet']
        json_data['average'] = getAverageRatingByPetId(json_data['id'])
        json_data['comments'] = getPetComments(json_data['id'])

    return json_data


def getPetComments(pet_id):
    json_data = json.dumps({
        'pet_id': pet_id
    })
    url = ENDPOINT_API + 'pet/comment'
    response = requests.get(url, data=json_data)
    json_data = json.loads(response.text)

    if 'comments' in json_data:
        json_data = json_data['comments']

    return json_data


@api.route('/api/user', methods=['GET'])
def user():
    username = request.args.get('username', '')
    if username == '':
        return 'No username provided', 400

    return getUser(username), 200


@api.route('/api/user/load', methods=['POST'])
def user_load():
    token = getLoginToken()
    if token == '':
        return 'Not logged in.', 403
    username = getUsernameForToken(token)
    if username == '':
        return 'Not logged in.', 403

    return getUser(username), 200


@api.route('/api/user/login', methods=['POST'])
def user_login():
    url = ENDPOINT_API + 'login'
    response = requests.post(url, json=request.json)
    response = json.loads(response.text)

    if response['match']:
        username = request.json['username']
        user = getUser(username)
        token = username
        user['logintoken'] = token
        return user

    return 'Username or password is invalid', 409


@api.route('/api/user/register', methods=['POST'])
def user_register():
    url = ENDPOINT_API + 'register'
    response = requests.post(url, json=request.json)
    response = json.loads(response.text)

    if response['success']:
        username = request.json['username']
        user = getUser(username)
        token = username
        user['logintoken'] = token
        return user

    return response['info'], 409


@api.route('/api/user/logout', methods=['POST'])
def user_logout():
    return "Logged out.", 200


@api.route('/api/user/update/bio', methods=['POST'])
def user_update_bio():
    token = getLoginToken()
    if token == '':
        return 'Not logged in.', 403
    username = getUsernameForToken(token)
    if username == '':
        return 'Not logged in.', 403

    json_data = json.dumps({
        'username': username,
        'new_bio': request.json['bio']
    })

    url = ENDPOINT_API + 'user/bio'
    requests.post(url, data=json_data)

    return 'Success', 200


@api.route('/api/user/update/email', methods=['POST'])
def user_update_email():
    token = getLoginToken()
    if token == '':
        return 'Not logged in.', 403
    username = getUsernameForToken(token)
    if username == '':
        return 'Not logged in.', 403

    json_data = json.dumps({
        'username': username,
        'new_email': request.json['email']
    })

    url = ENDPOINT_API + 'user/email'
    requests.post(url, data=json_data)

    return 'Success', 200


@api.route('/api/user/pets', methods=['POST'])
def user_pets():
    username = request.json['username']
    return getUserPets(username), 200


@api.route('/api/user/pets/rate', methods=['POST'])
def user_pets_rate():
    token = getLoginToken()
    if token == '':
        return 'Not logged in.', 403
    username = getUsernameForToken(token)
    if username == '':
        return 'Not logged in.', 403

    url = ENDPOINT_API + 'rating'
    json_data = json.dumps({
        'id': request.json['pet'] + username,
        'username': username,
        'rating': request.json['rating'],
        'pet_id': request.json['pet']
    })
    response = requests.post(url, data=json_data)
    json_data = json.loads(response.text)

    if json_data['success']:
        return 'Success', 200

    return 'Failed to rate pet', 400


@api.route('/api/user/pets/rated', methods=['POST'])
def user_pets_rated():
    username = request.json['username']
    return getRatedUserPets(username)


@api.route('/api/pet/add', methods=['POST'])
def pet_add():
    token = getLoginToken()
    if token == '':
        return 'Not logged in.', 403
    username = getUsernameForToken(token)
    if username == '':
        return 'Not logged in.', 403

    user = getUser(username)

    json_data = json.dumps({
        'pet_name': request.json['name'],
        'folder_name': 'pet_images',
        'image': request.json['image'],
        'username': username,
        'num_pets': user['num_pets']
    })

    url = ENDPOINT_API + 'add-pet'
    response = requests.post(url, json=json_data)
    json_data = json.loads(response.text)

    if json_data['success']:
        return 'Success', 200

    return 'Failed to add pet', 400


@api.route('/api/pet/', methods=['GET'])
def pet():
    pet_id = request.args.get('pet', '')
    if pet_id == '':
        return 'No pet provided', 400

    return getPet(pet_id), 200


@api.route('/api/pet/random', methods=['GET'])
def pet_random():
    return getRandomPet(), 200


@api.route('/api/pet/search', methods=['POST'])
def pet_search():
    json_data = json.dumps({
        'search': request.json['search']
    })
    url = ENDPOINT_API + 'search'
    response = requests.get(url, data=json_data)
    json_data = json.loads(response.text)

    if 'pets' in json_data:
        json_data = json_data['pets']

    return json_data, 200


@api.route('/api/pet/comments', methods=['GET'])
def pet_comments():
    pet_id = request.args.get('pet', '')
    if pet_id == '':
        return 'No pet provided', 400

    return getPetComments(pet_id), 200


@api.route('/api/pet/comment', methods=['POST'])
def pet_comment():
    token = getLoginToken()
    if token == '':
        return 'Not logged in.', 403
    username = getUsernameForToken(token)
    if username == '':
        return 'Not logged in.', 403

    json_data = json.dumps({
        'pet_id': request.json['pet'],
        'text': request.json['comment'],
        'username': username,
    })

    url = ENDPOINT_API + 'pet/comment'
    response = requests.post(url, json=json_data)
    json_data = json.loads(response.text)

    return 'Success', 200
