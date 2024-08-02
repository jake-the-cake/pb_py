from flask import Flask, render_template, request

app = Flask(__name__)

# 

links = [{
	'text': 'Home',
	'url': '/'
}, {
	'text': 'About',
	'url': 'about'
}]

def set_nav_data(links, active_path):
	for link in links:
		if link['url'] == active_path:
			link['active']= True
	return links

@app.route('/')
def home():
	nav = set_nav_data(links, request.path)

	return render_template('pb-home.html', meta = { 'page_title': 'Come With Us'}, nav = nav), 200