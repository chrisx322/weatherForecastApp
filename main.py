import streamlit as st
import plotly.express as px
from backend import get_data

# Add title, text input, slider, select box and subheader widgets
st.title("Weather Forecast for the Next Days")
place = st.text_input("Place: ")
days = st.slider("Forecast Days", min_value=1, max_value=5,
                 help="select the number of forecasted days")
option = st.selectbox("Select data to view",
                      ('Temperature', 'Sky'))

st.subheader(f"{option} for the next {days} days in {place}")

if place:
    # Get the temperature/sky data
    try:
        filtered_data = get_data(place, days)

        # Create temperature plot
        if option == "Temperature":
            temperatures = [dic["main"]["temp"] for dic in filtered_data]
            date = [dic["dt_txt"] for dic in filtered_data]
            figure = px.line(x=date, y=temperatures, labels={"x": "Date", "y": "Temperature (C)"})
            st.plotly_chart(figure)

        if option == "Sky":
            sky_conditions = [dic["weather"][0]["main"] for dic in filtered_data]
            images = {"Clear": "images/clear.png", "Clouds": "images/cloud.png",
                      "Rain": "images/rain.png", "Snow": "snow.png"}
            image_paths = [images[condition] for condition in sky_conditions]
            st.image(image_paths, width=115)
    except KeyError:
        st.write("The place you entered does not exist.")
