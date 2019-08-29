import os

from flask import Flask, session, json, current_app, redirect, url_for
from flask_assets import Environment
from flask_compress import Compress
from flask_login import LoginManager
from flask_mail import Mail
from flask_rq import RQ
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_moment import Moment
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from flask_babel import Babel, lazy_gettext as _l
from flask_ckeditor import CKEditor
from flask_cors import CORS, cross_origin
from flask_bcrypt import Bcrypt
# from oauth2client.contrib.flask_util import UserOAuth2


# from app.assets import app_css, app_js, vendor_css, vendor_js
from config import config

basedir = os.path.abspath(os.path.dirname(__file__))

mail = Mail()
db = SQLAlchemy()
csrf = CSRFProtect()
compress = Compress()
moment = Moment()
babel = Babel()
ckeditor = CKEditor()
cors = CORS()
flask_bcrypt = Bcrypt()
# Set up Flask-Login
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'account.login'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # not using sqlalchemy event system, hence disabling it

    app.config['OAUTH_CREDENTIALS'] = {
        'google': {
            'id': '',
            'secret': ''
        },
        'facebook': {
            'id': '',
            'secret': ''
        },
        'twitter': {
            'id': '',
            'secret': ''
        }
    }

    config[config_name].init_app(app)

    # Set up extensions
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    compress.init_app(app)
    moment.init_app(app)
    ckeditor.init_app(app)
    RQ(app)
    app.config['CORS_HEADERS'] = 'Content-Type'
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    flask_bcrypt.init_app(app)
    babel.init_app(app)

    photos = UploadSet('photos', IMAGES)
    configure_uploads(app, photos)
    patch_request_class(app)

    app.config['CKEDITOR_ENABLE_CSRF'] = True
    app.config['CKEDITOR_FILE_UPLOADER'] = '/admin/upload'

    # Register Jinja template functions
    from .utils import register_template_utils
    register_template_utils(app)

    # Set up asset pipeline
    assets_env = Environment(app)
    dirs = ['assets/styles', 'assets/scripts']
    for path in dirs:
        assets_env.append_path(os.path.join(basedir, path))
    assets_env.url_expire = True

    # Configure SSL if platform supports it
    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask.ext.sslify import SSLify
        SSLify(app)

    # # Create app blueprints

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    # customer blue_print

    # home blue_print

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    # publisher blue_print

    # home blue_print

    from .auth import account as account_blueprint
    app.register_blueprint(account_blueprint, url_prefix='/account')

    from .social import social as account_blueprint
    app.register_blueprint(account_blueprint, url_prefix='/social_login')

    # csrf.exempt(api_blueprint)

    from .api import blueprint as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/mobile')

    return app
