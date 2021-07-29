import numpy as np

import sqlalchemy
from sqlalchemy import engine
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, json, jsonify

Base = automap_base()

engine = create_engine("sqlite:///hawaii.sqlite")

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

  results = results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date > '2016-08-23)').\
    order_by(Measurement.date).all()

  session.close()
  
  all_precipitaiton = []
  
  for date, prcp in results:
      precipitation_dict = {}
      precipitation_dict['date'] = date
      precipitation_dict['prcp'] = prcp
      all_precipitaiton.append(precipitation_dict)

  return jsonify(all_precipitaiton)



if __name__ == '__main__':
    app.run(debug=True)



