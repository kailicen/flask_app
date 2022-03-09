from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from buddyship.config import Config
from flask_admin import Admin
from os import path
from datetime import date
from . import custom_template_filters


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'
mail = Mail()
admin = Admin(name='Buddyship Admin', template_mode='bootstrap3')


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    admin.init_app(app)

    from buddyship.users.routes import users
    from buddyship.auth.routes import auth
    from buddyship.main.routes import main
    from buddyship.progresses.routes import progresses
    from buddyship.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(progresses)
    app.register_blueprint(errors)
    register_template_filters(flask_app=app)

    create_database(app)

    return app


def register_template_filters(flask_app: Flask):
    flask_app.register_blueprint(custom_template_filters.blueprint)
    return None


def create_database(app):
    if not path.exists('buddyship/database.db'):
        db.create_all(app=app)
        from .models import User

        with app.app_context():
            admin_account = User(if_admin=True, first_name='admin', email='vppr-6247@toastmastersclubs.org',
                                 password=bcrypt.generate_password_hash(
                                     'admin').decode('utf-8'),
                                 active=True, confirmed_at=date.today())
            db.session.add(admin_account)
            db.session.commit()

        print('Created Database!')
