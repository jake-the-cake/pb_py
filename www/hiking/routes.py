from flask import request, render_template, jsonify
from app import app, db
from .links import links
from data.user.models import User

def set_nav_data(links, active_path):
	for link in links:
		if link['url'] == active_path: link['active']= True
		else: link['active'] = False
	return links


# 
# 
# 
# web routes
@app.route('/')
def home():
	nav = set_nav_data(links, request.path)
	# user = db.user.insert_one({})
	user = db.user.find_one({'first_name': 'Joe'})
	print(user)
	return render_template(
		'pb-home.html', 
		meta = { 'page_title': 'Come With Us'}, 
		nav = nav, 
		user = user
	), 200

@app.route('/about/')
def about():
	nav = set_nav_data(links, request.path)
	return render_template('pb-about.html', meta = { 'page_title': 'Come With Us'}, nav = nav), 200

@app.route('/tours/')
def tours():
	nav = set_nav_data(links, request.path)
	return render_template('pb-about.html', meta = { 'page_title': 'Come With Us'}, nav = nav), 200

@app.route('/gallery/')
def gallery():
	nav = set_nav_data(links, request.path)
	return render_template('pb-about.html', meta = { 'page_title': 'Come With Us'}, nav = nav), 200

@app.route('/blog/')
def blog():
	nav = set_nav_data(links, request.path)
	return render_template('pb-about.html', meta = { 'page_title': 'Come With Us'}, nav = nav), 200

# 
# 
# 
# api routes
@app.route('/api/user/new/', methods=['POST'])
def new_user():
	return User().new_user()

@app.route('/api/user/all/', methods=['GET'])
def get_all():
	return User().get()

@app.route('/api/user/remove/', methods=['GET'])
def remove_all():
	return User().remove()