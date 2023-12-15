# New York City Collision Analysis
This Repository contains visualizations about the NYC collisions in different borough and can be filtered according to the date.

# Streamlit Application Link
https://narendra17.streamlit.app/

# Introduction
The dataset used in this analysis contains information on vehicle collisions in NYC. It includes details such as the date and time of the incident, borough, street name, contributing factors, and geographical coordinates (latitude and longitude). The data spans from January 1, 2021, to April 9, 2023.
## Overview
The NYC Vehicle Collision Analysis Dashboard offers an intuitive and interactive platform for exploring and understanding various facets of vehicle collisions in New York City (NYC). Leveraging the NYC Collisions dataset, the dashboard provides insights into patterns, contributing factors, and geographic distribution of accidents.

### Features
Accidents By Date and Borough
Explore a geographical representation of accidents by date and borough using a collision map. Understand the spatial distribution of incidents over time.

### Contributing Factors for More Collisions
Analyze contributing factors to accidents, visualize a word cloud for the entire dataset, and filter data by specific contributing factors.

### Top Collision Locations
Discover the top collision locations and delve into details for a selected street name. Identify areas with a higher frequency of accidents.

### Heat Map
View a heatmap illustrating the distribution of collisions throughout the day. Understand the temporal patterns and peak hours of accidents.

### Collision Counts
Explore the trend of collision counts over a selected date range using a line chart. Identify trends and anomalies in accident frequency.

### Comparative Analysis
Compare collision counts between different boroughs or streets. Gain insights into the relative safety levels across various locations.

# Data Source
The New York City Collision Data has been taken from the Maven Analytics

The link for the dataset is:
https://mavenanalytics.io/data-playground?page=4&pageSize=10

# Data Pre-Processing and Cleaning
The raw data has a lot of unwanted and wrongly formatted data. So the main task after getting the dataset was to clean it and convert it into the format I need.
## Steps Performed in Data Pre-Processing and Cleaning:

1.converted the date entries to the datetime format and transformed the time entries to the timestamp format.
2.Additionally, we performed data cleaning by removing rows with missing values in the contributing factor column. 
3.Dropped the rows with null values in the 'Latitude' or 'Longitude' columns to ensure the data used for mapping is complete.These preprocessing steps enhance the dataset for better analysis and visualization in the Streamlit app.

# Future Work
In Future Iterations, I would like to add K-Means clustering to the analysis and mark the cluster on the map and I am looking forwad to make it real time as the  data gets updated the visualization gets updated.
