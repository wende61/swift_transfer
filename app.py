from http.client import INTERNAL_SERVER_ERROR, NOT_FOUND
from flask import Flask, render_template, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from sqlalchemy.orm import joinedload
from flask_seeder import FlaskSeeder
from extensions import db
app = Flask(__name__, template_folder="templates")
app.debug = True
# db = SQLAlchemy()

app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/swift_connect_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.options(joinedload(User.customer)).get(int(user_id))


from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from main import main as main_blueprint
app.register_blueprint(main_blueprint)

from customer import customer as customer_blueprint
app.register_blueprint(customer_blueprint)

from transfer import transfer as transfer_blueprint
app.register_blueprint(transfer_blueprint)


# Internal Server Error (HTTP 500) handler
@app.errorhandler(INTERNAL_SERVER_ERROR)
def handle_internal_server_error(error):
    return render_template('500.html'), 500

# Not Found (HTTP 404) handler
@app.errorhandler(NOT_FOUND)
def handle_not_found_error(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
    