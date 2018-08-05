
from flask import Flask
from flask_restful import reqparse, abort, Api, Resource, fields, marshal, marshal_with
from flask.ext.sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
api = Api(app)

#Model
################
class BookMark(db.Model):

	__tablename__ = "bookmarks"

	bookmark_id = db.Column(db.Integer, primary_key=True)
	bookmark_url = db.Column(db.String, nullable=False)

	def __init__(self, bookmark_url):
		self.bookmark_url = bookmark_url

	def __repr__(self):
		return '<bookmark_url {}>'.format(self.bookmark_url)


################

# Fields
bookmark_fields = {
	'bookmark_id' : fields.Integer,
	'bookmark_url' : fields.String,
	'uri' : fields.Url('bookmark',absolute=True, scheme='http')
	}


bookmarks_fields = {
	'bookmark_id' : fields.Integer,
	'bookmark_url' : fields.String,
	'uri' : fields.Url('bookmarks',absolute=True, scheme='http')
	}



class BookMarkAPI(Resource):



	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('bookmark_url', type=str, required=True, help='No bookmark url provided',location='json')
		super(BookMarkAPI, self).__init__()


	def get(self, bookmark_id):
		bmark_id = bookmark_id
		bookmark = db.session.query(BookMark).filter_by(bookmark_id = bmark_id).one()
		return {'bookmark': marshal(bookmark, bookmark_fields)}

	def delete(self, bookmark_id):
		bmark_id = bookmark_id
		db.session.query(BookMark).filter_by(bookmark_id=bmark_id).delete()
		db.session.commit()
		#return "delete a single bookmark"
		return {'result': True}

	@marshal_with(bookmarks_fields)
	def put(self, bookmark_id):

		args = self.reqparse.parse_args()
		updated_bookmark = str(args['bookmark_url'])
		bmark_id = bookmark_id

		db.session.query(BookMark).filter_by(bookmark_id=bmark_id).update({"bookmark_url": updated_bookmark})
		db.session.commit()
		return {'bookmark': updated_bookmark}



class BookMarksAPI(Resource):

	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('bookmark_url', type=str, required=True, help='No bookmark url provided',location='json')
		super(BookMarksAPI, self).__init__()


	def get(self):
		bookmarks = db.session.query(BookMark).all()
		return {'bookmarks': [marshal(bookmark, bookmark_fields) for bookmark in bookmarks]}



	def post(self):
		args = self.reqparse.parse_args()
		bookmark = BookMark(args['bookmark_url'])
		db.session.add(bookmark)
		db.session.commit()
		return {'bookmark': marshal(bookmark, bookmarks_fields)}

api.add_resource(BookMarksAPI, '/api/v1/bookmarks', endpoint = 'bookmarks')
api.add_resource(BookMarkAPI, '/api/v1/bookmark/<int:bookmark_id>', endpoint = 'bookmark')

if __name__ == '__main__':
    app.run(debug=True)
