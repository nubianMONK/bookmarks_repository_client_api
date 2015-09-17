from flask import Flask, render_template, request, redirect, url_for,flash,session,jsonify
import requests
from flask.ext.session import Session
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from flask.ext.sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_restful import abort
from forms import AddBookMark, EditBookMark



app = Flask(__name__)
app.config.from_object('config_web')


bootstrap = Bootstrap(app)
CsrfProtect(app)
bookmark_flask_session = Session


# Helper functions
def all_bookmarks():
	resp = requests.get('http://localhost:5000/api/v1/bookmarks')
	if resp.status_code != 200:
		flash('GET /bookmarks/ {}'.format(resp.status_code))
	bookmarks = resp.json()
	for k,v in bookmarks.items():
		sub_list = v
	return sub_list
		
	
	
def one_bookmark(uri):
	resp = requests.get(uri)
	if resp.status_code != 200:
		flash('GET /bookmark/ {}'.format(resp.status_code))
		abort(404, message="Bookmark does not exist".format(resp.status_code))
	bookmarks = resp.json()
	for k,v in bookmarks.items():
		sub_list = v
	return sub_list
	
		
# All bookmarks
@app.route('/api/v1/bookmarks/all', methods=['GET'])
def bookmarks():
    return render_template(
	'bookmarks.html',
	form=AddBookMark(request.form),
	all_bookmarks=all_bookmarks()
    )
	
	
# add a bookmark
@app.route('/api/bookmarks', methods=['GET','POST'])
def add_bookmark():
	form = AddBookMark(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			new_bookmark = form.bookmark_url.data
			bmark_uri = 'http://localhost:5000/api/v1/bookmarks'
			resp = requests.post(bmark_uri, json={'bookmark_url' : new_bookmark})
			if resp.status_code != 200:
				abort(404, message="Bookmark not added {}".format(resp.status_code))
			flash('New bookmark saved.')
			return render_template('bookmarks.html', form=form, all_bookmarks=all_bookmarks())
	return render_template('entry_bookmarks.html', form=form) 
	
	
# edit
@app.route('/api/v1/bookmark/edit/<path:uri>', methods=['GET','POST'])
def edit_bookmark(uri):
	form = EditBookMark(request.form)
	editable_bookmark = one_bookmark(uri)

	if request.method == 'POST':
		if form.validate_on_submit():
			updated_bookmark = str(form.bookmark_url.data)
			bmark_uri = uri
			resp = requests.put(bmark_uri, json={'bookmark_url' : updated_bookmark})
			if resp.status_code != 200:
				flash('PUT /bookmark/ {}'.format(resp.status_code))
				abort(404, message="Bookmark not updated")
			flash('BookMark Update is successful')
			return render_template('bookmarks.html', all_bookmarks=all_bookmarks())
	return render_template('edit_bookmarks.html', form=form,  editable_bookmark=editable_bookmark)
	


# delete
@app.route('/api/v1/bookmark/delete/<path:uri>',methods=['GET'])
def delete_bookmark(uri):
   	resp = requests.delete(uri)
	bookmarks = resp.json()
	for k,v in bookmarks.items():
		sub_list = v
	if sub_list and resp.status_code == 200:
		flash('The BookMark was successfully deleted.')
		return render_template('bookmarks.html', all_bookmarks=all_bookmarks())
	
	
	