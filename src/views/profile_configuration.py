from flask import request, render_template, Blueprint
from config import get_navbar_lang, login_required
import json

profile_configuration = Blueprint("profile_configuration", __name__, static_folder="static", template_folder="templates")

@profile_configuration.route('/config')
@login_required
def config_page():
        # read GET variable
    user = json.load( open("data/dummy/user.json") )
    if request.args.get("lang") == "es":
        # open config file according to the GET variable lang
        lang = json.load( open("static/config/es/config.json") )
    else:
        lang = json.load( open("static/config/en/config.json") )
    get_navbar_lang(lang)
    return render_template("config.html",lang=lang, user=user)