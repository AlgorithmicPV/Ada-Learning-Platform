"""
Landing Page of the application
"""

from flask import Blueprint, render_template

landing_page_bp = Blueprint("landing_page", __name__)


@landing_page_bp.route("/")
def landing_page():
    """
    Render the landing page.

    Returns:
        Response: Rendered HTML for 'landing/index.html'.
    """
    return render_template("landing/index.html")
