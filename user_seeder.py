from flask_seeder import Seeder
from models import User

class UserSeeder(Seeder):
 def run(self):
   if not User.query.count():
     user = User(username="wende", email="wende@gmail.com", role="admin")
     customer_user = User(username="abebe", email="abebe@gmail.com", role="customer")
     self.db.session.add(user)
     self.db.session.add(customer_user)