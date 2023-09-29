import streamlit as st
import openai
import os
import pandas as pd
import matplotlib.pyplot as plt
import random
from streamlit_folium import folium_static
from streamlit.components.v1 import html
import folium


from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Retrieve API key
openai.api_key = os.getenv("OPENAI_API_KEY")

from streamlit import components


import requests
import json

# UCF banner image
st.image("./UCF.jpg", width=600, caption="University of Central Florida")


def get_road_route(start_coords, end_coords):
    url = f"http://router.project-osrm.org/route/v1/driving/{start_coords[1]},{start_coords[0]};{end_coords[1]},{end_coords[0]}?overview=full&geometries=geojson"
    response = requests.get(url)
    data = json.loads(response.content)
    if data.get("routes"):
        route_coordinates = data["routes"][0]["geometry"]["coordinates"]
        route_coordinates = [(lat, lon) for lon, lat in route_coordinates]
        return route_coordinates
    else:
        return None


# Custom CSS to make the interface colorful
st.markdown(
    """
    <style>
        .reportview-container {
            background: linear-gradient(to bottom, #5d54a4, #9c95b8);
        }
        .sidebar .sidebar-content {
            background: linear-gradient(to bottom, #9c95b8, #5d54a4);
        }
        h1 {
            color: black;
        }
        h2 {
            color: black;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Streamlit App
st.title("🚨 Intelligent Disaster Response 🚨")

# Sidebar for navigation
st.sidebar.title("🌐 Navigation")
page = st.sidebar.selectbox(
    "Select a page", ["🏠 Home", "📦 Resource Allocation", "🗺️ Routing", "🌡️ Sensor Data"]
)


# Function to create a folium map with road-based routing
def create_map_with_route(start_coords, end_coords):
    m = folium.Map(location=start_coords, zoom_start=15)
    folium.Marker(start_coords, tooltip="Start").add_to(m)
    folium.Marker(end_coords, tooltip="End").add_to(m)

    route_coordinates = get_road_route(start_coords, end_coords)
    if route_coordinates:
        folium.PolyLine(route_coordinates, color="blue", weight=2.5, opacity=1).add_to(
            m
        )
    else:
        st.warning("Could not get road-based route.")

    return m


# Home page for real-time data analysis
if page == "🏠 Home":
    st.header("📊 Real-time Data Analysis 📊")

    # Collect mock real-time data
    social_media_data = st.text_input(
        "📱 Enter social media data", "Fire reported at location X"
    )
    sensor_data = st.text_input("🌡️ Enter sensor data", "Temperature: High, Wind: Low")
    news_data = st.text_input("📰 Enter news data", "Wildfire spreading rapidly")

    # Simulate LLM analysis
    if st.button("🔍 Analyze Data"):
        st.success("📋 Situation assessed. Immediate action required.")

# Page for resource allocation
elif page == "📦 Resource Allocation":
    st.header("📦 Resource Allocation 📦")

    # Collect mock resource data
    resources = st.text_input(
        "🚒 Enter available resources", "10 Firetrucks, 20 Ambulances"
    )

    # Simulate resource optimization
    if st.button("🔍 Optimize Resources"):
        st.success("📋 Resources optimized. Ready for deployment.")

# Page for routing
elif page == "🗺️ Routing":
    st.header("🗺️ Routing for Rescue Operations 🗺️")

    # Set default coordinates to University of Central Florida for start
    default_start = "28.6024, -81.2001"

    # Set default coordinates to Partnership II Building for end
    default_end = "28.5895, -81.1893"

    # Collect routing data
    start_location = st.text_input(
        "🅰️ Enter start location (latitude, longitude)", default_start
    )
    end_location = st.text_input(
        "🅱️ Enter end location (latitude, longitude)", default_end
    )

    start_coords = tuple(map(float, start_location.split(",")))
    end_coords = tuple(map(float, end_location.split(",")))

    # Simulate routing algorithm
    if st.button("🔍 Plan Route"):
        st.success("📋 Optimal route planned. Ready for action.")

        # Create and display the map
        m = create_map_with_route(start_coords, end_coords)
        html_data = m._repr_html_()
        st.components.v1.html(html_data, width=800, height=400)

# Page for Sensor Data
elif page == "🌡️ Sensor Data":
    st.header("🌡️ Sensor Data Integration 🌡️")

    # Collect mock sensor data
    weather_data = st.text_input(
        "🌦️ Enter weather data", "Temperature: 25°C, Humidity: 60%"
    )
    seismic_data = st.text_input("🌍 Enter seismic data", "Richter Scale: 2.5")
    other_sensor_data = st.text_input("🔬 Enter other sensor data", "Air Quality: Good")

    # Simulate data integration
    if st.button("🔍 Integrate Sensor Data"):
        st.success("📋 Sensor data integrated. Ready for analysis.")
