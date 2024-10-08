from flask import request, render_template
from app import app, db
from .links import links

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
	user = db.user.find_one({'first_name': 'Jason'})
	return render_template(
		'pb-home.html', 
		meta = { 'page_title': 'Come With Us'}, 
		nav = nav, 
		user = user
	), 200

@app.route('/about/')
def about():
	nav = set_nav_data(links, request.path)
	return render_template('pb-about.html', meta = { 'page_title': 'Who are we?'}, nav = nav), 200

@app.route('/tours/')
def tours():
	nav = set_nav_data(links, request.path)
	return render_template('pb-about.html', meta = { 'page_title': 'Plan your next adventure today'}, nav = nav), 200

@app.route('/gallery/')
def gallery():
	nav = set_nav_data(links, request.path)
	return render_template('pb-about.html', meta = { 'page_title': 'Scenes from our previous adventures'}, nav = nav), 200

@app.route('/blog/')
def blog():
	nav = set_nav_data(links, request.path)
	return render_template('pb-about.html', meta = { 'page_title': 'Come With Us'}, nav = nav), 200