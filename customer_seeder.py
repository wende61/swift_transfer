from flask_seeder import Seeder
from models import Customers

class CustomerSeeder(Seeder):
 def run(self):
   if not Customers.query.count():
     new_customer = Customers(
            first_name="abebe",
            last_name="buzu",
            customer_email="abebe@gmail.com",
            address="Addis Ababa",
            user_id=2 
        )
     self.db.session.add(new_customer)