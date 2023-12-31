import streamlit as st
import pandas as pd 
import altair as alt
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import folium
import plotly.express as px

# Load the dataset
@st.cache_data()    
def load_data():
    df = pd.read_csv('NYC_Collisions.csv')
    return(df)

data = load_data()

# Sidebar for user input
st.sidebar.title('Vehicle Collision Analysis in NYC')

# Set the minimum and maximum dates for date input
min_date = pd.to_datetime('2021-01-01')
max_date = pd.to_datetime('2023-04-09')
default_start_date = pd.to_datetime('2021-01-01')
default_end_date = pd.to_datetime('2021-01-15')

# Sidebar for user input
selected_date_range = st.sidebar.date_input(
    'Select Date Range',
    [default_start_date, default_end_date],
    min_value=min_date,
    max_value=max_date
)
forwarning = len(selected_date_range)

selected_borough = st.sidebar.selectbox('Select Borough', data['Borough'].unique())

#adding title and description about hte dataset
st.title("Visualization of NYC Collisions")
st.markdown("Welcome to the Vehicle Collision Analysis Dashboard for New York City (NYC). This interactive dashboard provides a comprehensive overview of vehicle collisions in NYC, allowing users to explore and analyze various aspects of traffic incidents.")
    # Function to filter data with caching
if forwarning >= 2:
    def filter_data(data, selected_date_range, selected_borough):
        start_date, end_date = pd.to_datetime(selected_date_range[0]), pd.to_datetime(selected_date_range[1])

        # Convert 'Date' column to datetime type
        data['Date'] = pd.to_datetime(data['Date'])

        # Filter data based on user input
        filtered_data = data[
            (data['Date'].between(start_date, end_date)) & 
            (data['Borough'] == selected_borough)
        ]

        return filtered_data

    # Filter data based on user input
    filtered_data = filter_data(data.copy(), selected_date_range, selected_borough)



# Check if both start and end dates are selected

    # Convert 'Date' column to datetime type
    data['Date'] = pd.to_datetime(data['Date'])

    # Convert date type to datetime64[ns]
    selected_date_range = [pd.to_datetime(date) for date in selected_date_range]

   

    # Drop rows with null values in 'Latitude' or 'Longitude'
    filtered_data = filtered_data.dropna(subset=['Latitude', 'Longitude'])

    # Display selected information
    st.write(f'Selected Date Range: {selected_date_range[0].date()} to {selected_date_range[1].date()}')



    tab1, tab2,tab4, tab5,tab6,tab7 = st.tabs(["Accidents By date and Borough", "contributing factors for more collisions", "Top Collision Locations","Heat map","collision counts","camparision"])
    with tab1:
    # Map
        st.title('Collision Map')
        st.write("This tab provides a geographical representation of accidents by date and borough using a collision map.")
       

        # Create a copy with required column names
        map_data = filtered_data[['Latitude', 'Longitude']].copy()

        # Rename columns to match the expected names
        map_data = map_data.rename(columns={'Latitude': 'lat', 'Longitude': 'lon'})

        # Display the map
        st.map(map_data)

    with tab6:
        st.header("collision counts over the selected date range")
        st.write("Explore the trend of collision counts over the selected date range using a line chart.")

        
        # Line chart for trend over time
        chart = alt.Chart(filtered_data).mark_line().encode(
            x='Date:T',
            y='count()',
            tooltip=['Date:T', 'count()']
        ).properties(width=800, height=500)

        # Display the chart
        st.altair_chart(chart)
    
    # with tab3:
    #     # Contributing Factors Analysis
    #     st.title('Contributing Factors Analysis')



    #     # Bar chart illustrating the distribution of contributing factors
    #     contributing_factors_distribution = filtered_data_no_unspecified['Contributing Factor'].value_counts()
    #     st.bar_chart(contributing_factors_distribution)


    with tab4:
         # Top Collision Locations Analysis
        st.title('Top Collision Locations')
        st.write("Explore the top collision locations and view details for a selected street name.")

        # Group by street name and count collisions
        top_locations = filtered_data.groupby('Street Name').size().reset_index(name='Collision Count')

        # Sort and get the top locations
        top_locations = top_locations.sort_values(by='Collision Count', ascending=False).head(10)

        # Allow users to filter by borough or specific street names
        selected_location = st.selectbox('Select a Street Name', top_locations['Street Name'])
        filtered_by_location = filtered_data[filtered_data['Street Name'] == selected_location]


        #st.dataframe(filtered_by_location)
        # Display top collision locations
        st.table(top_locations)

        # Display related collision details for the selected location
        st.subheader(f'Details for Street Name: {selected_location}')
        #st.dataframe(filtered_by_location)
        
        street_counts = filtered_by_location['Street Name'].value_counts()

        # Create a DataFrame from the counts
        street_counts_df = pd.DataFrame({'Street Name': street_counts.index, 'Count': street_counts.values})

        # Display the DataFrame
        st.dataframe(street_counts_df)

    with tab5:
        # Time-of-Day Analysis
        st.title('Time-of-Day Analysis')
        st.write("Explore the distribution of collisions throughout the day and view details for a selected time range.")
        # Convert the 'Time' column to datetime type
        filtered_data['Time'] = pd.to_datetime(filtered_data['Time'], errors='coerce')

        # Allow users to filter by specific hours or time ranges
        selected_hour = st.slider('Select Hour', 0, 23, (0, 23))
        # Filter data based on the selected time range
        filtered_by_hour = filtered_data[
            (filtered_data['Time'].dt.hour >= selected_hour[0]) & 
            (filtered_data['Time'].dt.hour <= selected_hour[1])
        ]


        # Display heatmap or line chart for the distribution of collisions throughout the day
        chart_type = st.radio('Select Chart Type', ['Heatmap', 'Line Chart'])

        if chart_type == 'Heatmap':
            # Heatmap for the distribution of collisions throughout the day
            heatmap_data = filtered_by_hour.groupby(['Time']).size().reset_index(name='Collision Count')
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

    with tab2:
        # Wordcloud for contributing factors from the entire dataset
        st.title('Contributing Factors')
        st.write("Explore contributing factors to accidents, view a word cloud for the entire dataset, and filter by a specific contributing factor.")

        data = data[data['Contributing Factor'] != 'Unspecified']
        text = ' '.join(data['Contributing Factor'].astype(str))

        # Plot the word cloud
        st.markdown(f"###### Contributing Factors Word Cloud for the Entire Dataset")
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        st.pyplot(plt)

        filtered_data_no_unspecified = filtered_data[filtered_data['Contributing Factor'] != 'Unspecified']
        
        contributing_factors_distribution = filtered_data_no_unspecified['Contributing Factor'].value_counts()
        # Allow users to select a specific contributing factor
        selected_factor = st.selectbox('Select a Contributing Factor', contributing_factors_distribution.index)

        # Exclude 'Unspecified' from contributing factors
        filtered_data_no_unspecified = filtered_data[filtered_data['Contributing Factor'] != 'Unspecified']

        # Display related collision details
        selected_factor_details = filtered_data_no_unspecified[filtered_data_no_unspecified['Contributing Factor'] == selected_factor]
        st.dataframe(selected_factor_details)



    with tab7:
        # Comparative Analysis
        st.title('Comparative Analysis')
        st.write("Compare collision counts between different boroughs or streets.")


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
