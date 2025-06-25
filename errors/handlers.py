from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def not_found(error):
    return render_template("error.html", message="Page not found."), 404

@errors.app_errorhandler(403)
def forbidden(error):
    return render_template("error.html", message="Access denied."), 403
