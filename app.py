import datetime as dt
import numpy as np

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# MY INSTRUCTOR PROVIDED STARTER CODE 
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(autoload_with=engine)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)



@app.route("/")
def welcome():
    return (
        f"Hawaii Climate Analysis API<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/start/end<br/>"
        f"<p> The 'start' and'end' dates should be in MMDDYYYY format.</p>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data for the last year"""
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    session.close()
    
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)


@app.route("/api/v1.0/stations")
def stations():
    """Return the station data for the last year"""
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    stations = session.query(Measurement.date, Measurement.station)\
        .filter(Measurement.date >= prev_year).all()
    session.close()

    stationq = {date: station for date, station in stations}
    return jsonify(stationq)


@app.route("/api/v1.0/tobs")
def tobs():
    """Return the temperature data for the last year"""
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    temperature = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= prev_year).all()
    session.close()

    tempq = {date: tobs for date, tobs in temperature}
    return jsonify(tempq)


@app.route("/api/v1.0/<start>")
def temp_start(start):
    start_temperature = session.query(func.min(Measurement.tobs), 
                                      func.max(Measurement.tobs), 
                                      func.avg(Measurement.tobs))\
        .filter(Measurement.date >= start)\
        .group_by(Measurement.tobs).all()
    session.close()

    all_temp_start = []
    for minimum, maximum, average in start_temperature:
        all_temp_start_dict = {}
        all_temp_start_dict["minimum"] = minimum
        all_temp_start_dict["maximum"] = maximum
        all_temp_start_dict["average"] = average
        all_temp_start.append(all_temp_start_dict)

    return jsonify(all_temp_start)



@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start, end):
    temperature_se = session.query(func.min(Measurement.tobs), 
                                   func.max(Measurement.tobs), 
                                   func.avg(Measurement.tobs))\
        .filter(Measurement.date >= start)\
        .filter(Measurement.date < end)\
        .group_by(Measurement.date).all()
    session.close()

    all_temp_start_end = []
    for minimum, maximum, average in temperature_se:
        all_temp_start_end_dict = {}
        all_temp_start_end_dict["minimum"] = minimum
        all_temp_start_end_dict["maximum"] = maximum
        all_temp_start_end_dict["average"] = average
        all_temp_start_end.append(all_temp_start_end_dict)

    return jsonify(all_temp_start_end)


if __name__ == "__main__":
    app.run(debug=True)
