

from views import db
from models import BookMark

db.create_all()

db.session.commit()
