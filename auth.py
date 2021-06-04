from flask import Flask, Blueprint, render_template, session, redirect, url_for, request, flash

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.route('/login')
def login():
	return render_template('login.html')
	
	
@auth.route('/register')
def register():
	return render_template('register.html')