# SQLalchemy_Challenge

For this assignment, the following will be analyzed:

## Climate Analysis and Exploration

Python and SQLAlchemy will be used for basic climate analysis and data exploration of the climate database. All of the following analysis will be completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.

### Precipitation Analysis

For this analysis, the following will be executed:

- Design a query to retrieve the last 12 months of precipitation data.
- Select only the date and prcp values.
- Load the query results into a Pandas DataFrame and set the index to the date column.
- Sort the DataFrame values by date.
- Plot the results using the DataFrame plot method.
- Use Pandas to print the summary statistics for the precipitation data.

### Station Analysis

For this analysis, the following will be executed:

- Design a query to calculate the total number of stations.
- Design a query to find the most active stations.
    - List the stations and observation counts in descending order.
    - Find the station with the highest number of observations.
- Design a query to retrieve the last 12 months of temperature observation data (tobs).
    - Filter by the station with the highest number of observations.
    - Plot the results as a histogram with bins=12.

### Temperature Analysis I

- Identify the average temperature in June and December at all stations across all available years in the dataset. 
- Use the t-test to determine whether the difference in the means, if any, is statistically significant. 

### Temperature Analysis II

- Using the function called calc_temps, find the minimum, average, and maximum temperatures for dates of trip using the matching dates from the previous year.
- Plot the min, avg, and max temperature from the previous query as a bar chart.
    - Use the average temperature as the bar height.
    - Use the peak-to-peak (tmax-tmin) value as the y error bar (yerr).

### Daily Rainfall and Temperature Average

- Calculate the rainfall per weather station using the previous year's matching dates.
- Calculate the daily normals. Normals are the averages for the min, avg, and max temperatures.
- Use the function daily_normals to calculate the daily normals for a specific date. This date string will be in the format %m-%d. All historic tobs that match that date string will be included.
- Create a list of dates for the trip in the format %m-%d. Use the daily_normals function to calculate the normals for each date string and append the results to a list.
- Load the list of daily normals into a Pandas DataFrame and set the index equal to the date.
- Use Pandas to plot an area plot (stacked=False) for the daily normals.


---------------------------------------------------------------------------------

## Climate App

Design a Flask API based on the above queries.

Routes:
- /
    - Home page.
    - List all routes that are available.

- /api/v1.0/precipitation
    - Convert the query results to a Dictionary using date as the key and prcp as the value.
    - Return the JSON representation of the dictionary.

- /api/v1.0/stations
    - Return a JSON list of stations from the dataset.

- /api/v1.0/tobs
    - Query for the dates and temperature observations from a year from the last data point.
    - Return a JSON list of Temperature Observations (tobs) for the previous year.

- /api/v1.0/<start> and /api/v1.0/<start>/<end>
    - Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
    - When given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date.
    - When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

---------------------------------------------------------------------------------

Along with what we learned in class, I also used the following resources to complete this assignment:

- https://stackoverflow.com/
- https://www.geeksforgeeks.org/
- https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_rel.html
- https://libguides.library.kent.edu/SPSS/PairedSamplestTest
- https://pandas.pydata.org/pandas-docs/version/0.23.4/generated/pandas.DataFrame.plot.html
- https://flask.palletsprojects.com/en/1.1.x/errorhandling/
- https://docs.sqlalchemy.org/en/13/index.html
