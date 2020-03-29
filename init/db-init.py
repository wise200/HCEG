from app import db
from app.models import User
from sys import argv

admin = User(username='admin')
admin.set_password(argv[1])
assert(admin.check_password(argv[2])i) # must type admin password twice for safety
db.session.add(admin)
db.session.commit()

