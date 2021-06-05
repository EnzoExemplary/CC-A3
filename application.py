from flask import Flask, Blueprint, render_template, session, request, flash, url_for, redirect
from auth import auth
from util import getUsername, getUserByUsername
import requests
import json

application = Flask(__name__)
application.config['SECRET_KEY'] = "\x07/\xc2\xbc\xfd\xb9\xb3<\x1f\xd40\xef3\x92\x01\xeb&\xbd\x8f\xe8r\xc3\xb6"
application.register_blueprint(auth)

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

if __name__ == "__main__":
	application.debug = True
	application.run()
	