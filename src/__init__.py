from flask import Flask
import config
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
config.oauth = OAuth(app)