import os
from werkzeug.utils import secure_filename
from flask import Flask, jsonify, request, render_template, redirect, url_for

app = Flask(  # Create a flask app
	__name__,
	template_folder='templates',  # Name of html file folder
	static_folder='static'  # Name of directory for static files
)

IMAGE_LOCATION = r'images/'


app.config['UPLOAD_FOLDER'] = IMAGE_LOCATION
IMAGE_NAMES =[]
for path in os.listdir(IMAGE_LOCATION):
	IMAGE_NAMES.append(f"{IMAGE_LOCATION}{path}")
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

#User dictionary {username : password}
users = {"Roy" : "yes"}


facebook_friends=["loaf","bread","monkey see", "monkey doo", "monkey stare", "monkey eat"]

def allowed_file(filename):
    return filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])  # '/' for the default page
def login():
	if request.method == 'POST':
		for key in users:
			if key == request.form['username'] and users[key] == request.form['password']:
				for user in users:
					if user not in facebook_friends and user not in request.form['username']:
						facebook_friends.append(user)
				return redirect(url_for('home'))

		return render_template('login.html', wrong=True, error="Wrong username or password")
	else:
		return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		if request.form['username'] in users:
			return render_template('register.html', wrong=True, error="Username already exists")
		else:
			users[request.form['username']] = request.form['password']
			return redirect(url_for('login', wrong=False))
	else:
		return render_template('register.html')

@app.route('/home')
def home():
	return render_template(
		'home.html',
		friends = facebook_friends)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
		file = request.files['file']
		if file is not None and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			return redirect(url_for('home'))
		else:
			for path in os.listdir(IMAGE_LOCATION):
				if path not in IMAGE_NAMES: IMAGE_NAMES.append(f"{IMAGE_LOCATION}{path}")
			return render_template('upload.html', wrong=True, error="Wrong file type", images=IMAGE_NAMES)
	else:
		for path in os.listdir(IMAGE_LOCATION):
			if path not in IMAGE_NAMES: IMAGE_NAMES.append(f"{IMAGE_LOCATION}{path}")
		return render_template('upload.html', images=IMAGE_NAMES)

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