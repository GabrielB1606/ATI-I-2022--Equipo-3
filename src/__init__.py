from flask import Flask
import config
from authlib.integrations.flask_client import OAuth

# Initialize Flask main App
app = Flask(__name__)
app.config['SECRET_KEY'] = '123'
app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O/<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

# Initialize OAuth module
config.oauth = OAuth(app)