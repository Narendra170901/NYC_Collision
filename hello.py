import streamlit as st
import pandas as pd 
import altair as alt

data = pd.read_csv("Average_Daily_Traffic_Counts.csv")
st.dataframe(data)


# Streamlit app
st.title('Bar Chart')

# Altair bar chart
bar_chart = alt.Chart(data).mark_bar().encode(
    x='Date of Count',
    y='Total Passing Vehicle Volume'
)

# Display the Altair chart using st.altair_chart
st.altair_chart(bar_chart, use_container_width=True)