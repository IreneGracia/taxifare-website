import streamlit as st
import requests
from datetime import datetime

# Title for the app
st.title('Taxi Fare Prediction')

# Section header
st.header("Enter the details of your ride")

# 1. Date and time of the ride
ride_date = st.date_input("Select the ride date", value=datetime.now().date())
ride_time = st.time_input("Select the ride time", value=datetime.now().time())

# Combine ride_date and ride_time into a single datetime object
combined_datetime = datetime.combine(ride_date, ride_time)

# Format the datetime object into the required format: "YYYY-MM-DD HH:MM:SS"
pickup_datetime = combined_datetime.strftime("%Y-%m-%d %H:%M:%S")

# 2. Pickup location (longitude and latitude)
st.subheader("Pickup Location")
pickup_longitude = st.number_input("Pickup Longitude", value=0.0, format="%.6f")
pickup_latitude = st.number_input("Pickup Latitude", value=0.0, format="%.6f")

# 3. Dropoff location (longitude and latitude)
st.subheader("Dropoff Location")
dropoff_longitude = st.number_input("Dropoff Longitude", value=0.0, format="%.6f")
dropoff_latitude = st.number_input("Dropoff Latitude", value=0.0, format="%.6f")

# 4. Passenger count
passenger_count = st.number_input("Passenger Count", min_value=1, max_value=10, value=1)

# Button to submit the form
if st.button("Submit"):
    # Display the input values
    # st.write(f"Ride Date: {ride_date}")
    # st.write(f"Ride Time: {ride_time}")
    # st.write(f"Pickup Location: ({pickup_latitude}, {pickup_longitude})")
    # st.write(f"Dropoff Location: ({dropoff_latitude}, {dropoff_longitude})")
    # st.write(f"Passenger Count: {passenger_count}")


    url = 'https://taxifare-177918934575.europe-west1.run.app/predict'

    params={"pickup_datetime":pickup_datetime,
            "pickup_longitude":pickup_longitude,
            "pickup_latitude":pickup_latitude,
            "dropoff_longitude":dropoff_longitude,
            "dropoff_latitude":dropoff_latitude,
            "passenger_count":passenger_count}

    response = requests.get(url, params=params)
    response_data = response.json()

    st.write(response_data['fare'])
