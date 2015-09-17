from flask.ext.wtf import Form
from wtforms.fields import StringField, SubmitField,IntegerField, HiddenField
from wtforms.validators import Required,URL


class AddBookMark(Form):
	bookmark_url = StringField('Bookmark URL',[URL(require_tld=False, message='Not a Valid URL')])
	form_submit = SubmitField('Add Bookmark')

class EditBookMark(Form):
	bookmark_url = StringField('Bookmark URL',[URL(require_tld=False, message='Not a Valid URL')])
	form_submit = SubmitField('Update')
	
	
	