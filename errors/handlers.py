from flask import Blueprint, render_template

errors = Blueprint("errors", __name__)


@errors.app_errorhandler(404)
def not_found(error):
    return render_template(
        "error.html", message="Page not found.", error_code=404), 404


@errors.app_errorhandler(403)
def forbidden(error):
    return render_template(
        "error.html", message="Access denied.", error_code=403), 403


@errors.app_errorhandler(405)
def methods_not_allowed(error):
    return render_template(
        "error.html", message="Methods are not allowed.", error_code=405), 405


# TODO: Still not done with outher error types
# TODO: Keep the navigation thing in the error page 
# after user signed

# table names should be Camelcase and row like pythin varaibles