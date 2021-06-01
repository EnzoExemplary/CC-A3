from flask import Flask, Blueprint, render_template, session, request, flash, url_for, redirect
from auth import auth

application = Flask(__name__)
application.config['SECRET_KEY'] = "+-fY6PsEWdPHZeWxD8T.]P}{K,96Wp6!"
application.register_blueprint(auth)

@application.route('/')
def root():
	return render_template('index.html')	

if __name__ == "__main__":
	application.debug = True
	application.run()