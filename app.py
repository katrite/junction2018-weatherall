from flask import jsonify, Flask, render_template, request
from flask_cors import CORS
import json
import logging
import os

from integrations import citybikes
from integrations import vaisala

STATIONS_LIST = json.load(open("data/stations.json", "r"))
MOCK_STATION_STATS = json.load(
    open("data/citybike-stations-2018-11-24-1316.json", "r")
)  # TODO replace with real availability/prediction data
logger = logging.getLogger(__name__)

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object("config")
CORS(app)

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


@app.route("/api/weather_sensor_readings", methods=["GET"])
def get_weather_sensor_readings():
    """
    Return the latest Vaisala device readings.
    """
    res = vaisala.get_latest_reading()
    return jsonify(res)


@app.route("/api/bikestations", methods=["GET"])
def list_station_stats():
    """
    List all bike stations along with location, number of bikes and predicted
    demand for bikes
    """
    return jsonify(MOCK_STATION_STATS)


@app.route("/api/livestations", methods=["GET"])
def list_live_station_stats():
    stations = citybikes.list_stations()
    return jsonify({"stations": stations})


@app.route("/api/stations", methods=["GET"])
def list_stations():
    """
    List all stations along with name, coordinates etc.
    """
    return jsonify(STATIONS_LIST)


# Error handlers.


@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "not found"}), 404


@app.errorhandler(Exception)
def internal_error(error):
    logger.exception(error)
    return jsonify({"error": "unhandled server error"}), 500


# Or specify port manually:
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
