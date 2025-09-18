# To avoid circular import error in authentication
from authlib.integrations.flask_client import OAuth

oauth = OAuth()
