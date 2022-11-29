from flask import Blueprint, send_file
from config import image_saver

image_collection = Blueprint("image_collection", __name__, static_folder="static", template_folder="templates")

# demo for fetching mongoDB data
@image_collection.route('/<filename>')
def fetch_users_image(filename):
    if( filename.split(".")[-1] == "png" ):
        mimetype="image/png"
    else:
        mimetype="image/jpeg"
        
    return send_file( image_saver.get_last_version(filename), mimetype=mimetype )