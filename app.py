from flask import jsonify, Flask, render_template, request
import logging
import os

logger = logging.getLogger(__name__)

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object("config")

# Automatically tear down SQLAlchemy.
"""
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
"""

# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api", methods=["GET"])
def api_root():
    return jsonify({})


# Error handlers.


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "not found"}), 404


@app.errorhandler(Exception)
def internal_error(error):
    logger.error(error)
    return jsonify({"error": error.status}), error.status or 500


# Default port:
if __name__ == "__main__":
    app.run()

# Or specify port manually:
"""
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
"""
