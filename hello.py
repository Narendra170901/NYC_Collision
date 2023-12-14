!pip install wordcloud

from wordcloud import WordCloud

import streamlit as st
import pandas as pd 
import altair as alt
import matplotlib.pyplot as plt
import folium

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

    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Accidents By date and Borough", "Type of Collisions", "Suicide Statistics", "Age and Gender Statistics"])

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
        st.header("Type of Collisions occurred more")

        # Convert 'Contributing Factor' column to strings and join them
        text = ' '.join(filtered_data['Contributing Factor'].astype(str))

        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

        # Plot the word cloud
        st.markdown(f"###### Contributing Factors for {selected_borough}")

        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        st.pyplot(plt)

        # Display the filtered data
        st.write(filtered_data)

else:
    st.warning("Please select a valid date range.")
