import datetime as dt
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite", connect_args={"check_same_thread": False})

# Reflect an existing database into a new model

Base = automap_base()

# Reflect the tables

Base.prepare(engine, reflect=True)

# Save reference to the table

Measurement = Base.classes.measurement
Station = Base.classes.station

# Set variables to be used later

session = Session(engine)

last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

year_start_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

app = Flask(__name__)

@app.route("/")
def welcomepage():
    """List all routes that are available"""
    return(
        f"<center><h1><b>Hawaii Climate Information</b></h1></center>"

        f"<center><h1>(Data available from January 1st, 2010 to August 23, 2017)</h1></center>"

        f"Available Routes:<br/>"

        f"/api/v1.0/precipitation<br/>"
        f"Dates and Precipitation Data from 2016-08-24 to 2017-08-23<br/><br/>"

        f"/api/v1.0/stations<br/>"
        f"List of Hawaii weather stations with station ID, info, latitude, longitude, and elevation<br/><br/>"

        f"/api/v1.0/tobs<br/>"
        f"List of Temperature Observations(tobs) from 2016-08-24 to 2017-08-23<br/><br/>"

        f"/api/v1.0/yyyy-mm-dd/<br/>"
        f"Provide start date to get Average, Maximum, and Minimum Temperatures. Date must be provided in YYYY-MM-DD format.<br/><br/>"

        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd/<br/>"
        f"Provide start and end date to get Average, Maximum, and Minimum Temperatures. Dates must be provided in YYYY-MM-DD format."
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return dates and precipitation data from 2016-08-24 to 2017-08-23."""
    
    # Query all precipitation measurements for above year

    precip_query = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date > year_start_date).all()
    
    # Create a dictionary from the row data and append to a list of all precipitation data

    precip_data = []

    for date, prcp in precip_query:
        precip_dict = {}
        precip_dict["Date"] = date
        precip_dict["Precipitation"] = prcp
        precip_data.append(precip_dict)

    # Return data in json format

    return jsonify(precip_data)

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of all Hawaii stations"""

    # Query all station data 

    station_data = session.query(Station.station, Station.name, Station.latitude, Station.longitude, Station.elevation).all()

    # Create a dictionary from the row data and append to a list of all stations

    station_list = []

    for station, name, latitude, longitude, elevation in station_data:
        s_data = {}
        s_data['Station ID'] = station
        s_data['Station Info'] = name
        s_data['Latitude'] = latitude
        s_data['Longitude'] = longitude
        s_data['Elevation'] = elevation
        station_list.append(s_data)
    
    # Return data in json format

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def temp_obs():
    """Return a list of tobs from the 2016-08-24 to 2017-08-23"""

    # Query temperature data with date

    temp_query = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > year_start_date).all()
    
    # Create a dictionary from the row data and append to a list of all temperature data

    temp_data = []

    for date, tobs in temp_query:
        temp_dict = {}
        temp_dict["Date"] = date
        temp_dict["Temperature"] = tobs
        temp_data.append(temp_dict)

    # Return data in json format

    return jsonify(temp_data)

@app.route('/api/v1.0/<start_date>/')
def temp_for_start_date(start_date):
    """Return the avg, max, and min temp for all dates greater than or equal to start date provided"""

    # Query for temperature data for specific time frame

    start_date_data = session.query(Measurement.date, func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).filter(Measurement.date >= start_date).order_by(Measurement.date.desc()).all()
    
    # Create a dictionary from the row data and append to a list of temperature data for start date provided until end date
    # Label the start and end date with () and use "Begin" so that the returned dictionary has the dates in the beginning
    start_temp_data = []

    for date, avg_temp, max_temp, min_temp in start_date_data:
        start_temp_dict = {}
        start_temp_dict["(Begin Date)"] = date
        start_temp_dict["(End Date)"] = "2017-08-23"
        start_temp_dict["Average Temperature"] = float(start_date_data[0][1])
        start_temp_dict["Highest Temperature"] = float(start_date_data[0][2])
        start_temp_dict["Lowest Temperature"] = float(start_date_data[0][3])
        start_temp_data.append(start_temp_dict)

    # Return data in json format

    return jsonify(start_temp_data)

@app.route('/api/v1.0/<start_date>/<end_date>/')
def date_range(start_date, end_date):
    """Return the avg, max, min, temp over date range provided"""

    # Query temperature data for date range provided

    date_range_data = session.query(func.avg(Measurement.tobs), func.max(Measurement.tobs), func.min(Measurement.tobs)).filter(Measurement.date >= start_date, Measurement.date <= end_date).all()
    
    # Create a dictionary from the row data and append to a list of temperature data for start and end date provided
    # Label the start and end date with () and use "Begin" so that the returned dictionary has the dates in the beginning
    
    date_rate_list = []
    for avg_temp, max_temp, min_temp in date_range_data:
        range_data = {}
        range_data["(Begin Date)"] = start_date
        range_data["(End Date)"] = end_date
        range_data["Average Temperature"] = float(date_range_data[0][0])
        range_data["Highest Temperature"] = float(date_range_data[0][1])
        range_data["Lowest Temperature"] = float(date_range_data[0][2])
        date_rate_list.append(range_data)
    
    # Return data in json format

    return jsonify(date_rate_list)

if __name__ == '__main__':
    app.run(debug=True)