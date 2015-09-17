#from bookmarks_api import app



class BookMark(db.Model):
	
	__tablename__ = "bookmarks"
	
	bookmark_id = db.Column(db.Integer, primary_key=True)
	bookmark_url = db.Column(db.String, nullable=False)
	
	def __init__(self, bookmark_url):
		self.bookmark_url = bookmark_url
		
	def __repr__(self):
		return '<bookmark_url {}>'.format(self.bookmark_url)
