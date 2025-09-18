from flask import Blueprint, render_template

errors = Blueprint("errors", __name__)


@errors.app_errorhandler(404)
def not_found(error):
    """
    This error handler is used when a page is not found (404).
    It shows the error.html template with the message
    "Page not found." and returns the 404 status code.
    """
    return render_template(
        "error.html", message="Page not found.", error_code=404), 404


@errors.app_errorhandler(403)
def forbidden(error):
    """
    This error handler is used when access is denied (403).
    It shows the error.html template with the message
    "Access denied." and returns the 403 status code.
    """
    return render_template(
        "error.html", message="Access denied.", error_code=403), 403


@errors.app_errorhandler(405)
def methods_not_allowed(error):
    """
    This error handler is used when a method is not allowed (405).
    It shows the error.html template with the message
    "Methods are not allowed." and returns the 405 status code.
    """
    return render_template(
        "error.html", message="Methods are not allowed.", error_code=405), 405
