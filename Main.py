import streamlit as st
import requests
import matplotlib.pyplot as plt
import pandas as pd

api_key = "61715cca62d140abab9181719241912"
current_url = "http://api.weatherapi.com/v1/current.json"
forecast_url = "http://api.weatherapi.com/v1/forecast.json"

st.title(":green[Live] :blue[Weather] Dashboard 🌦️⚡")

city = st.text_input("Enter a City:")

# You will learn about this Function later in the code
def emoji_func(cond):
    if "lear" in condition:
        emoji = "🌙"
    elif "Sunny" in condition:
        emoji = "☀️"
    elif "Cloudy" in condition:
        emoji = "☁️"
    elif "rain" in condition:
        emoji = "🌧️"
    elif "Rain" in condition:
        emoji = "🌧️"
    else:   
        emoji = ""
    return emoji
left, right = st.columns(2, gap="small", vertical_alignment="top")
if left.button("Get Weather"):
    params = {"key": api_key, "q": city}
    response_current = requests.get(current_url, params=params)
    params = {"key": api_key, "q": city, "days": 1}
    response_forecast =requests.get(forecast_url, params=params)

    if response_current.status_code == 200:
        data = response_current.json()
        cast = response_forecast.json()

        location = data["location"]["name"]
        country = data["location"]["country"]
        condition = data["current"]["condition"]["text"]
        temp = data["current"]["temp_c"]
        feels_like = data["current"]["feelslike_f"]
        feels_like = round((feels_like - 32) * 5/9, 1)
        humidity = data["current"]["humidity"]
        wind_speed = data["current"]["wind_kph"]

        hourly_forecast = cast["forecast"]["forecastday"][0]["hour"]
        hours = [hour["time"][-5:] for hour in hourly_forecast]  # Extract time (HH:MM)
        temps = [hour["temp_c"] for hour in hourly_forecast]  # Extract temperature
        conditions = [hour["condition"]["text"] for hour in hourly_forecast]  # Extract conditions

        st.subheader(f"Weather in {location}, {country}")
        col1, col2, col3, col4, col5 = st.columns(5)
        col3.metric(label="**Condition**", value=f"{condition}{emoji_func(cond=condition)}")
        st.divider()
        col1, col2, col3, col4 = st.columns(4)
        col1.metric(label="Temperature", value=f"{temp} °C")
        col2.metric(label="Feels Like", value=f"{feels_like} °C")
        col3.metric(label="Humidity", value=f"{humidity} %")
        col4.metric(label="Wind Speed", value=f"{wind_speed} km/h")

        # Display Hourly Forecast Table
        st.subheader("24-Hour Forecast")
        hourly_data = {
            "Time": hours,
            "Temperature (°C)": temps,
            "Condition": conditions,
        }
        df = pd.DataFrame(hourly_data).T
        st.dataframe(df, use_container_width=True)

        

        st.divider()

         # Create the plot
        fig, ax = plt.subplots(figsize=(10, 6))  # Adjust figure size
    

        # Plot the data
        ax.plot(
            hours, 
            temps, 
            marker="o", 
            markersize=8, 
            color="royalblue", 
            linestyle="-", 
            linewidth=2, 
            alpha=0.9, 
            label="Temperature (°C)"
        )

        # Enhance labels and title
        ax.set_xlabel("Time (24-Hours)", fontsize=14, labelpad=10)
        ax.set_ylabel("Temperature (°C)", fontsize=14, labelpad=10)
        ax.set_title("24-Hour Temperature Trend", fontsize=16, pad=20, weight='bold')

        # Style the axes and background
        ax.set_facecolor('#f0f0f0')  # Set a slightly lighter gray for the plot background
        for location in ['left', 'right', 'top', 'bottom']:
            ax.spines[location].set_visible(False)  # Hide the spines

        # Add a grid
        ax.grid(visible=True, which='major', linestyle='--', linewidth=0.6, alpha=0.7, color="gray")

        # Improve ticks
        plt.xticks(rotation=45, ha="right", fontsize=12)
        plt.yticks(fontsize=12)

        # Add legend
        ax.legend(loc="upper left", fontsize=12, frameon=False)

        # Tighten layout and display
        plt.tight_layout()
        st.pyplot(fig)

    else:
            st.error("City not found or API request failed. Please try again.")

if right.button("Forecast"):
    params = {"key": api_key, "q": city, "days": 10}
    response = requests.get(forecast_url, params=params)

    if response.status_code == 200:
        cast = response.json()

        forecast_data = cast["forecast"]["forecastday"]

        location = cast["location"]["name"]
        country = cast["location"]["country"]
        st.subheader(f"10 Days Weather Forecasting for {location}, {country}")
        st.divider()

        date_list = []
        avg_temp_list = []
        for i in range(10): 
            
            date = forecast_data[i]["date"]
            avg_temperature = forecast_data[i]["day"]["avgtemp_c"]
            max_temperature = forecast_data[i]["day"]["maxtemp_c"]
            min_temperature = forecast_data[i]["day"]["mintemp_c"]
            wind_speed = forecast_data[i]["day"]["maxwind_kph"]
            condition = forecast_data[i]["day"]["condition"]["text"]
            
            date_list.append(date)
            avg_temp_list.append(avg_temperature)
            
            st.write(f"**Date**: {date}")
            st.write(f"**Average Temperature:** :green[{avg_temperature}] °C")
            st.write(f"**Max Temperature:** :red[{max_temperature}] °C")
            st.write(f"**Min Temperature:**:blue[{min_temperature}] °C")
            st.write(f"**Wind Speed:** {wind_speed} km/h")
            st.write(f"**Condition:** {condition}{emoji_func(cond=condition)}")
            with st.expander("Hourly Forecasting"):
                hourly_forecast = cast["forecast"]["forecastday"][0]["hour"]
                hours = [hour["time"][-5:] for hour in hourly_forecast]  # Extract time (HH:MM)
                temps = [hour["temp_c"] for hour in hourly_forecast]  # Extract temperature
                conditions = [hour["condition"]["text"] for hour in hourly_forecast]  # Extract conditions

                # Display Hourly Forecast Table
                st.subheader("24-Hour Forecast")
                hourly_data = {
                    "Time": hours,
                    "Temperature (°C)": temps,
                    "Condition": conditions,
                }
                df = pd.DataFrame(hourly_data).T
                st.dataframe(df,use_container_width=True)

                # Create the plot
                fig, ax = plt.subplots(figsize=(10, 6))  # Adjust figure size
               

                # Plot the data
                ax.plot(
                    hours, 
                    temps, 
                    marker="o", 
                    markersize=8, 
                    color="royalblue", 
                    linestyle="-", 
                    linewidth=2, 
                    alpha=0.9, 
                    label="Temperature (°C)"
                )

                # Enhance labels and title
                ax.set_xlabel("Time (24-Hours)", fontsize=14, labelpad=10)
                ax.set_ylabel("Temperature (°C)", fontsize=14, labelpad=10)
                ax.set_title("24-Hour Temperature Trend", fontsize=16, pad=20, weight='bold')

                # Style the axes and background
                ax.set_facecolor('#f0f0f0')  # Set a slightly lighter gray for the plot background
                for location in ['left', 'right', 'top', 'bottom']:
                    ax.spines[location].set_visible(False)  # Hide the spines

                # Add a grid
                ax.grid(visible=True, which='major', linestyle='--', linewidth=0.6, alpha=0.7, color="gray")

                # Improve ticks
                plt.xticks(rotation=45, ha="right", fontsize=12)
                plt.yticks(fontsize=12)

                # Add legend
                ax.legend(loc="upper left", fontsize=12, frameon=False)

                # Tighten layout and display
                plt.tight_layout()
                st.pyplot(fig)
              
            st.divider()
        
        fig, ax = plt.subplots(figsize=(10, 6))  # Adjust figure size
        ax.plot(
            date_list, 
            avg_temp_list, 
            marker="o", 
            markersize=8, 
            color="tomato", 
            linestyle="-", 
            linewidth=2, 
            alpha=0.8, 
            label="Avg Temp"
        )

        # Enhancing labels and title
        ax.set_xlabel("Days", fontsize=14, labelpad=10)
        ax.set_ylabel("Temperature (°C)", fontsize=14, labelpad=10)
        ax.set_title("10 Days Temperature Trend", fontsize=16, pad=20, weight='bold')

        # Hide spines
        for location in ['left', 'right', 'top', 'bottom']:
            ax.spines[location].set_visible(False)

        # Adding grid
        ax.grid(visible=True, which='major', linestyle='--', linewidth=0.5, alpha=0.7)

        # Improve ticks
        plt.xticks(rotation=45, ha="right", fontsize=10)
        plt.yticks(fontsize=10)

        # Add legend
        ax.legend(loc="upper left", fontsize=12)

        plt.tight_layout()
        st.pyplot(fig)