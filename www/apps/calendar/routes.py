from app import app
from www.hiking.routes import set_nav_data
from www.hiking.links import links
from flask import render_template, request
from data.calendar.build import use_calendar
from data.calendar.models import Calendar

@app.route('/calendar/')
def main():
	c = Calendar().get()
	print(c)
	cal = use_calendar()
	nav = set_nav_data(links, request.path)

	return render_template(
		'calendar.html', 
		meta = { 'page_title': 'Come With Us'}, 
		nav = nav,
		cal = cal
	), 200 