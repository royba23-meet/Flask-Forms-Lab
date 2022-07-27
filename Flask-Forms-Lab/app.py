import re
from flask import Flask, jsonify, request, render_template, redirect, url_for
import random

app = Flask(  # Create a flask app
	__name__,
	template_folder='templates',  # Name of html file folder
	static_folder='static'  # Name of directory for static files
)


username = "roy"
password = "yes"
facebook_friends=["loaf","bread","monkey see", "monkey doo", "monkey stare", "monkey eat"]


@app.route('/', methods=['GET', 'POST'])  # '/' for the default page
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		if username == "roy" and password == "yes":
			return redirect(url_for('home'))
		else:
			return render_template('login.html', error="Invalid username or password")
	else:
		return render_template('login.html')

@app.route('/home')
def home():
	return render_template(
		'home.html',
		friends = facebook_friends)

@app.route('/friend_exists/<string:friend>', methods=['GET', 'POST'])
def friend_exists(friend):
	return render_template(
		'friend_exists.html',
		friend=friend,
		isFriend = friend in facebook_friends)



if __name__ == "__main__":  # Makes sure this is the main process
	app.run( # Starts the site
    debug=True
	)