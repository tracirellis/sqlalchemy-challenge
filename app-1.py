# Import the dependencies.

import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model

base = automap_base()


# reflect the tables
base.prepare(engine, reflect= True)

# Save references to each table

station = base.classes.station
measurement = base.classes.measurement



#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all availble api routes"""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start year<br/>"
        f"/api/v1.0/start year/endyear<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = session(engine)
    """Return a list of all precipiation data for the year 2017"""
    # query preceipitation data for the year 2017 and exclude null values
    results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= '2017-01-01').\
        filter(measurement.date <= '2017-12-31').\
        filter(measurement.prcp.isnot(None)).all()
    
    session.close

    #convert the query results to a dictionary

    all_precipitation = {date: prcp for date, prcp in results}

    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def stations ():
    session = session(engine)
    """Return a list of all stations"""
    #query all stations
    results = session.query(station.station).all()
    session.close()

#convert list of tuples into normal list

    all_stations = list(np.ravel(results))
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = session(engine)
    active_stations = session.query(measurement.station, func.count(measurement.station)).\
        group_by(measurement.station).\
        order_by(func.count(measurement.station).desc()).all()
    
    """Return alist of all tobs for the year 2016"""
    results = session.query(measurement.station, measurement.date, measurement.tobs).\
        filter(measurement.date >= '2016-01-01').\
        filter(measurement.date <= '2016-12-31').\
        filter(measurement.station == active_stations[0][0]).all()
    
    session.close()

    #convert list of tuples into normal list

    all_tobs = []
    for station, date, tobs in results:
        tobs_dict = {}
        tobs_dict['station'] = station
        tobs_dict['date'] = date
        tobs_dict['tobs'] = all_tobs.append(tobs_dict)
    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start(start):
    session = session(engine)
    """Return a list of all tobs"""
    results = session.query(measurement.station, measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).\
        group_by(measurement.station, measurement.date).all()
    
    session.close()

    all_start = []
    for station, date, min_temp, avg_temp, max_temp in results:
        start_dict = {}
        start_dict["date"] = date
        start_dict["station"] = station
        start_dict["min_temp"] = min_temp
        start_dict["avg_temp"] = avg_temp
        start_dict["max_temp"] = max_temp
        all_start.append(start_dict)
    
    return jsonify(all_start)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = session(engine)
    """Return a list of all tobs"""
    results = session.query(measurement.station, measurement.date, func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >=start).\
        filter(measurement.date <= end + '-12-31').\
        group_by(measurement.station, measurement.date).all()
    
    session.close()

    all_start_end = []
    for station, date, min_temp, avg_temp, max_temp in results:
        start_end_dict = {}
        start_end_dict['station'] = station
        start_end_dict['date']= date
        start_end_dict['min_temp'] = min_temp
        start_end_dict['avg_temp'] = avg_temp
        start_end_dict['max_temp'] = max_temp
        all_start_end.append(start_end_dict)
    return jsonify(all_start_end)

if __name__ == '__main__':
    app.run(debug=-True)
    
