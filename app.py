# Import dependancies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify



# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement 

# Flask Setup
app = Flask(__name__)


# Flask Routes
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/prcp<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/tobs"
    )

@app.route("/api/v1.0/prcp")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all prcp values"""
    # Query the precipitation values
    results = session.query(Measurement.prcp, Measurement.date).all()

    session.close()

     # Create a dictionary from the row data and append to a list of all_values
    all_values = []
    for prcp, date in results:
        values_dict = {}
        values_dict["prcp"] = prcp
        values_dict["date"] = date
        all_values.append(values_dict)
        

    return jsonify(all_values)


@app.route("/api/v1.0/station")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query results
    results = session.query(Measurement.station).all()
    
    session.close()
    
     # Convert list of tuples into normal list
      
    all_stations = list(np.ravel(results))
    print(all_stations)
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query results
    
    results = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
    filter(Measurement.station == "USC00519397").\
    filter(Measurement.date >'2016-08-23').\
    order_by(Measurement.date).all()
    
    session.close()
    
    all_tobs = []
    for station, date, tobs in results:
        tobs_dict = {}
        tobs_dict["station"] = station
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        all_tobs.append(tobs_dict)
    return jsonify(all_tobs)

# Doesn't work..

if __name__ == '__main__':
    app.run(debug=True)