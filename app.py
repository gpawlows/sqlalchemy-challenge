import numpy as np

import sqlalchemy
from sqlalchemy import engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, json, jsonify

Base = automap_base()

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base.prepare(engine, reflect=True)

Station = Base.classes.station
Measurement = Base.classes.measurement

app = Flask(__name__)

@app.route("/")
def welcome():
    """List all avialable API routes."""
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    """Retun a list of data for the most recent year's worth of collected data on Hawaii precipitation"""

    results = results = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date > '2016-08-23)').\
      order_by(Measurement.date).all()

    session.close()
  
    # all_precipitaiton = []
  
    # for date, prcp in results:
    #     precipitation_dict = {}
    #     precipitation_dict['date'] = date
    #     precipitation_dict['prcp'] = prcp
    #     all_precipitaiton.append(precipitation_dict)

    all_precipitation = {date: prcp for date, prcp in results}



    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)

    """Return a list of all of the weather stations on Hawaii"""

    results = session.query(Station.name).all()

    session.close()

    all_stations = []

    for name in results:
        stations_dict = {}
        stations_dict["name"] = name
        all_stations.append(stations_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    """Returns the tempurtures from the most active station for the most recent year of data recorded"""
    
    most_active_station = 'USC00519281'
    results = session.query(Measurement.tobs).\
    filter_by(station=most_active_station).\
    filter(Measurement.date > '2016-08-17').\
    order_by(Measurement.date).all()

    session.close()

    all_tobs = []

    for tob in results:
        tobs_dict ={}
        tobs_dict["tobs"] = tob
        all_tobs.append(tobs_dict)
    
    return jsonify(all_tobs)




  


if __name__ == '__main__':
    app.run(debug=True)



