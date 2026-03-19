import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    trips = pd.read_csv("datasets/trips.csv")
    cars = pd.read_csv("datasets/cars.csv")
    cities = pd.read_csv("datasets/cities.csv")
    return trips, cars, cities

trips, cars, cities = load_data()

# Merge trips with cars
trips_merged = trips.merge(cars, left_on="car_id", right_on="id")

# Merge with cities
trips_merged = trips_merged.merge(cities, on="city_id")

# Update date format
trips_merged['pickup_date'] = pd.to_datetime(trips_merged['pickup_time']).dt.date

# Sidebar filter
cars_brand = st.sidebar.multiselect("Select the Car Brand", trips_merged['brand'].unique())
if cars_brand:
    trips_merged = trips_merged[trips_merged['brand'].isin(cars_brand)]

# Metrics
total_trips = len(trips_merged)
total_distance = trips_merged['distance'].sum()
top_car = trips_merged.groupby('model')['revenue'].sum().idxmax()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Trips", value=total_trips)
with col2:
    st.metric(label="Top Car Model by Revenue", value=top_car)
with col3:
    st.metric(label="Total Distance (km)", value=f"{total_distance:,.2f}")

# Preview
st.write(trips_merged.head())

# Visualizations
st.subheader("Trips Over Time")
st.line_chart(trips_merged.groupby('pickup_date').size())

st.subheader("Revenue Per Car Model")
st.bar_chart(trips_merged.groupby('model')['revenue'].sum())

st.subheader("Revenue by City")
st.bar_chart(trips_merged.groupby('city_name')['revenue'].sum())