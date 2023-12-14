import streamlit as st
import pandas as pd 
import altair as alt
import matplotlib.pyplot as plt
import plotly.express as px

# Load the dataset
data = pd.read_csv("NYC_Collisions.csv")
st.dataframe(data)

# Sidebar for user input
st.sidebar.title('Vehicle Collision Analysis in NYC')

# Set the minimum and maximum dates for date input
min_date = pd.to_datetime('2021-01-01')
max_date = pd.to_datetime('2023-04-09')
selected_date_range = st.sidebar.date_input('Select Date Range', [min_date, max_date], min_value=min_date, max_value=max_date)
selected_borough = st.sidebar.selectbox('Select Borough', data['Borough'].unique())

# Function to filter data with caching
@st.cache_data
def filter_data(data, selected_date_range, selected_borough):
    start_date, end_date = pd.to_datetime(selected_date_range[0]), pd.to_datetime(selected_date_range[1])

    # Filter data based on user input
    filtered_data = data[
        (data['Date'].between(start_date, end_date)) & 
        (data['Borough'] == selected_borough)
    ]

    return filtered_data

# Check if both start and end dates are selected
if len(selected_date_range) == 2:
    # Convert 'Date' column to datetime type
    data['Date'] = pd.to_datetime(data['Date'])

    # Convert date type to datetime64[ns]
    selected_date_range = [pd.to_datetime(date) for date in selected_date_range]

    # Filter data based on user input
    filtered_data = filter_data(data.copy(), selected_date_range, selected_borough)

    # Drop rows with null values in 'Latitude' or 'Longitude'
    filtered_data = filtered_data.dropna(subset=['Latitude', 'Longitude'])

    # Display selected information
    st.write(f'Selected Date Range: {selected_date_range[0].date()} to {selected_date_range[1].date()}')



    tab1, tab2, tab3,tab4, tab5,tab6,tab7 = st.tabs(["Accidents By date and Borough", "Line chart", "Bar Chart","Top Collision Locations","Heat map","contributing factors over time","camparision"])
    with tab1:
    # Map
        st.title('Collision Map')

        # Create a copy with required column names
        map_data = filtered_data[['Latitude', 'Longitude']].copy()

        # Rename columns to match the expected names
        map_data = map_data.rename(columns={'Latitude': 'lat', 'Longitude': 'lon'})

        # Display the map
        st.map(map_data)

    with tab2:
        st.header("Line chart")

        
        # Line chart for trend over time
        chart = alt.Chart(filtered_data).mark_line().encode(
            x='Date:T',
            y='count()',
            tooltip=['Date:T', 'count()']
        ).properties(width=800, height=500)

        # Display the chart
        st.altair_chart(chart)
    
    with tab3:

            # Contributing Factors Analysis
            st.title('Contributing Factors Analysis')

            # Bar chart illustrating the distribution of contributing factors
            contributing_factors_distribution = filtered_data['Contributing Factor'].value_counts()
            st.bar_chart(contributing_factors_distribution)

            # Allow users to select a specific contributing factor
            selected_factor = st.selectbox('Select a Contributing Factor', contributing_factors_distribution.index)

            # Display related collision details
            selected_factor_details = filtered_data[filtered_data['Contributing Factor'] == selected_factor]
            st.dataframe(selected_factor_details)
    with tab4:
         # Top Collision Locations Analysis
        st.title('Top Collision Locations')

        # Group by street name and count collisions
        top_locations = filtered_data.groupby('Street Name').size().reset_index(name='Collision Count')

        # Sort and get the top locations
        top_locations = top_locations.sort_values(by='Collision Count', ascending=False).head(10)

        # Allow users to filter by borough or specific street names
        selected_location = st.selectbox('Select a Street Name', top_locations['Street Name'])
        filtered_by_location = filtered_data[filtered_data['Street Name'] == selected_location]

        # Display top collision locations
        st.table(top_locations)

        # Display related collision details for the selected location
        st.subheader(f'Details for Street Name: {selected_location}')
        st.dataframe(filtered_by_location)

    with tab5:
        # Time-of-Day Analysis
        st.title('Time-of-Day Analysis')
        # Convert the 'Time' column to datetime type
        filtered_data['Time'] = pd.to_datetime(filtered_data['Time'], errors='coerce')

        # Allow users to filter by specific hours or time ranges
        selected_hour = st.slider('Select Hour', 0, 23, (0, 23))
        filtered_by_hour = filtered_data[(filtered_data['Time'].dt.hour >= selected_hour[0]) & (filtered_data['Time'].dt.hour <= selected_hour[1])]

        # Display heatmap or line chart for the distribution of collisions throughout the day
        chart_type = st.radio('Select Chart Type', ['Heatmap', 'Line Chart'])

        if chart_type == 'Heatmap':
            # Heatmap for the distribution of collisions throughout the day
            heatmap_data = filtered_data.groupby(['Time']).size().reset_index(name='Collision Count')
            heatmap_chart = alt.Chart(heatmap_data).mark_rect().encode(
                x='hours(Time):O',
                y='minutes(Time):O',
                color='Collision Count:Q',
                tooltip=['hours(Time):O', 'minutes(Time):O', 'Collision Count:Q']
            ).properties(width=800, height=500)
            st.altair_chart(heatmap_chart)
        else:
            # Line chart for the distribution of collisions throughout the day
            line_chart = alt.Chart(filtered_data).mark_line().encode(
                x=alt.X('Time:T', title='Time of Day'),
                y='count()',
                tooltip=['Time:T', 'count()']
            ).properties(width=800, height=500)
            st.altair_chart(line_chart)

        # Display filtered data based on the selected time range
        st.subheader(f'Details for Selected Time Range: {selected_hour[0]}:00 to {selected_hour[1]}:00')
        st.dataframe(filtered_by_hour)

    with tab6:
  
        # Contributing Factor Trends Over Time
        st.title('Contributing Factor Trends Over Time')

        # Allow users to select a specific contributing factor
        selected_contributing_factor = st.selectbox('Select Contributing Factor', data['Contributing Factor'].unique())

        # Filter data for the selected contributing factor
        filtered_by_contributing_factor = filtered_data[filtered_data['Contributing Factor'] == selected_contributing_factor]

        # Line chart for trends over time for the selected contributing factor
        contributing_factor_chart = alt.Chart(filtered_by_contributing_factor).mark_line().encode(
            x='Date:T',
            y='count()',
            tooltip=['Date:T', 'count()']
        ).properties(width=800, height=500)

        # Display the chart
        st.altair_chart(contributing_factor_chart)

        # Display related collision details for the selected contributing factor
        st.subheader(f'Details for Contributing Factor: {selected_contributing_factor}')
        st.dataframe(filtered_by_contributing_factor)


    with tab7:
        # Comparative Analysis
        st.title('Comparative Analysis')

        # Allow users to choose between comparing boroughs or streets
        comparison_type = st.radio('Select Comparison Type', ['Boroughs', 'Streets'])

        if comparison_type == 'Boroughs':
            # Bar chart for collision count comparison between different boroughs
            borough_comparison_chart = alt.Chart(filtered_data).mark_bar().encode(
                x='Borough:N',
                y='count()',
                tooltip=['Borough:N', 'count()']
            ).properties(width=800, height=500)

            # Display the chart
            st.altair_chart(borough_comparison_chart)

        elif comparison_type == 'Streets':
            # Allow users to select specific streets for comparison
            selected_streets = st.multiselect('Select Streets for Comparison', filtered_data['Street Name'].unique())

            # Filter data for the selected streets
            filtered_by_streets = filtered_data[filtered_data['Street Name'].isin(selected_streets)]

            # Bar chart for collision count comparison between selected streets
            streets_comparison_chart = alt.Chart(filtered_by_streets).mark_bar().encode(
                x='Street Name:N',
                y='count()',
                tooltip=['Street Name:N', 'count()']
            ).properties(width=800, height=500)

            # Display the chart
            st.altair_chart(streets_comparison_chart)

            # Display related collision details for the selected streets
            st.subheader('Details for Selected Streets')
            st.dataframe(filtered_by_streets)


else:
    st.warning("Please select a valid date range.")
