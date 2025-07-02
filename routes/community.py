from flask import Blueprint, session, redirect, url_for, request, jsonify, render_template

community_bp = Blueprint("community", __name__)

# Route that displays all community discussions that happened in the platform
@community_bp.route("/community")
def all_community_discussion():
    if "user_id" in session:
        return render_template("user/community/community_base.html")
    else:
        return redirect(url_for("auth.login"))

# Route that displays all community discussions that happened on one day
@community_bp.route("/community/newest")
def newest_community_discussion():
    if "user_id" in session:
        return render_template("user/community/community_base.html")
    else:
        return redirect(url_for("auth.login"))
    
# Routes that displays all discussion that have done by the user
@community_bp.route("/community/you")
def your_community_discussion():
    if "user_id" in session:
        return render_template("user/community/community_base.html")
    else:
        return redirect(url_for("auth.login"))

# Route that displays all community discussions that have not been answered
@community_bp.route("/community/unanswered")
def unanswered_community_discussion():
    if "user_id" in session:
        return render_template("user/community/community_base.html")
    else:
        return redirect(url_for("auth.login"))

# Route that displays all community discussions that have been saved by the user
@community_bp.route("/community/saved")
def saved_community_discussion():
    if "user_id" in session:
        return render_template("user/community/community_base.html")
    else:
        return redirect(url_for("auth.login"))