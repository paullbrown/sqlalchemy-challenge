from flask import Flask, jsonify

import datetime as dt
import numpy as np

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


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
        f"<p> The 'start' and'end' dates should be in the format MMDDYYYY.</p>"

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
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    stations = session.query(Measurement.date, Measurement.station).\
        filter(Measurement.date >= prev_year).all()

    session.close()
    
    station_result = {date: station for date, station in stations}
    return jsonify(station_result) 


@app.route("/api/v1.0/tobs")
def tobs():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temperature = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= prev_year).all()
    
    session.close()
    
    tobs_result = {date: tobs for date, tobs in temperature}
    return jsonify(tobs_result)


@app.route("/api/v1.0/temp/start/<temp_start>")
def temp_start():
    temperature_start = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date == temp_start).all()
    
    session.close()

    ts = {date: <temp_start_end> for date, tobs in temperature}
    return jsonify(ts)



@app.route("/api/v1.0/temp/start/end/<temp_start_end>")
def temp_start_end():
    temperature_start_end = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date == temp_start_end).all()
        

    session.close()

    tse = {date: <temp_start_end> for date, tobs in temperature}
    return jsonify(tse)








# don't forget...
if __name__ == "__main__":
    app.run(debug=True)
