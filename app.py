
import streamlit as st
import requests
from datetime import datetime
import pandas as pd
import pydeck as pdk  # Import pydeck

# Title for the app
st.title('Taxi Fare Prediction')

# Section header
st.header("Enter the details of your ride")

# 1. Date and time of the ride
ride_date = st.date_input("Select the ride date", value=datetime.now().date())
ride_time = st.time_input("Select the ride time", value=datetime.now().time())

# Combine ride_date and ride_time into a single datetime object
try:
    combined_datetime = datetime.combine(ride_date, ride_time)
except ValueError:
    combined_datetime = None

# Format the datetime object into the required format: "YYYY-MM-DD HH:MM:SS"
pickup_datetime = combined_datetime.strftime("%Y-%m-%d %H:%M:%S") if combined_datetime else None

# 2. Pickup location (longitude and latitude)
st.subheader("Pickup Location")
pickup_longitude = st.number_input("Pickup Longitude", value=0.0, format="%.6f")
pickup_latitude = st.number_input("Pickup Latitude", value=0.0, format="%.6f")

# 3. Dropoff location (longitude and latitude)
st.subheader("Dropoff Location")
dropoff_longitude = st.number_input("Dropoff Longitude", value=0.0, format="%.6f")
dropoff_latitude = st.number_input("Dropoff Latitude", value=0.0, format="%.6f")

# 4. Passenger count
passenger_count = st.number_input("Passenger Count", value=1)

# Validation
error_messages = []

# Latitude and Longitude checks
if not 40.5 <= pickup_latitude <= 40.9:
    error_messages.append("Pickup latitude must be between 40.5 and 40.9.")
if not 40.5 <= dropoff_latitude <= 40.9:
    error_messages.append("Dropoff latitude must be between 40.5 and 40.9.")
if not -74.3 <= pickup_longitude <= -73.7:
    error_messages.append("Pickup longitude must be between -74.3 and -73.7.")
if not -74.3 <= dropoff_longitude <= -73.7:
    error_messages.append("Dropoff longitude must be between -74.3 and -73.7.")

# Passenger count validation
if passenger_count <= 0 or passenger_count > 8:
    error_messages.append("Passenger count must be between 1 and 8.")

# Date and time validation
if combined_datetime is None:
    error_messages.append("Invalid date or time provided.")
elif combined_datetime < datetime.now():
    error_messages.append("Pickup date and time cannot be in the past.")

# Display error messages if any
if error_messages:
    for error in error_messages:
        st.error(error)
else:
    # Button to submit the form
    if st.button("Submit"):

        # API URL
        url = 'https://taxifare-177918934575.europe-west1.run.app/predict'

        # Parameters for the API
        params = {
            "pickup_datetime": pickup_datetime,
            "pickup_longitude": pickup_longitude,
            "pickup_latitude": pickup_latitude,
            "dropoff_longitude": dropoff_longitude,
            "dropoff_latitude": dropoff_latitude,
            "passenger_count": passenger_count,
        }

        # API request
        response = requests.get(url, params=params)
        response_data = response.json()

        # Display fare prediction
        st.write(f"Predicted Fare: ${response_data['fare']:.2f}")

        # Create DataFrame for map visualisation
        df = pd.DataFrame(
            {
                "lat": [pickup_latitude, dropoff_latitude],
                "lon": [pickup_longitude, dropoff_longitude],
            },
        )

        # Display map
        st.map(df)

        # Create a Pydeck map
        view_state = pdk.ViewState(
            latitude=(pickup_latitude + dropoff_latitude) / 2,  # Center the map
            longitude=(pickup_longitude + dropoff_longitude) / 2,
            zoom=10,  # Adjust zoom level
            pitch=30,
        )

        # Layer for showing points on the map
        layer = pdk.Layer(
            "ScatterplotLayer",
            df,
            get_position='[lon, lat]',
            get_fill_color='[255, 0, 0]',  # Colour for the points
            get_radius=500,  # Radius of the points in meters
        )

        # Render the Pydeck map
        r = pdk.Deck(map_style="mapbox://styles/mapbox/light-v9", initial_view_state=view_state, layers=[layer])
        st.pydeck_chart(r)
