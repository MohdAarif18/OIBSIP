import tkinter as tk
from tkinter import messagebox
import requests

# YOUR WEATHERAPI KEY
API_KEY = "1ac76daa7cc34c69be7152309261301"
BASE_URL = "https://api.weatherapi.com/v1/current.json"


def get_weather():
    city = city_entry.get().strip()

    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name.")
        return

    params = {
        "key": API_KEY,
        "q": city
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.HTTPError:
        messagebox.showerror("Error", "City not found.")
        return
    except requests.exceptions.RequestException:
        messagebox.showerror("Error", "Network error.")
        return

    # Extract weather data (WeatherAPI format)
    city_name = data["location"]["name"]
    country = data["location"]["country"]
    condition = data["current"]["condition"]["text"]
    temperature = data["current"]["temp_c"]
    feels_like = data["current"]["feelslike_c"]
    humidity = data["current"]["humidity"]
    wind = data["current"]["wind_kph"]
    pressure = data["current"]["pressure_mb"]

    # Update UI
    result_label.config(
        text=f"Weather in {city_name}, {country}\n{condition}"
    )
    temp_label.config(text=f"Temperature: {temperature} °C")
    feels_label.config(text=f"Feels Like: {feels_like} °C")
    humidity_label.config(text=f"Humidity: {humidity}%")
    wind_label.config(text=f"Wind Speed: {wind} km/h")
    pressure_label.config(text=f"Pressure: {pressure} mb")


# ---------------- GUI ---------------- #

root = tk.Tk()
root.title("Advanced Weather App")
root.geometry("420x420")
root.resizable(False, False)

tk.Label(
    root,
    text="🌦️ Weather Application",
    font=("Arial", 18, "bold")
).pack(pady=10)

frame = tk.Frame(root)
frame.pack(pady=5)

tk.Label(frame, text="City Name:").grid(row=0, column=0, padx=5, pady=5)
city_entry = tk.Entry(frame, width=25)
city_entry.grid(row=0, column=1)

tk.Button(
    root,
    text="Get Weather",
    width=20,
    command=get_weather
).pack(pady=10)

result_label = tk.Label(
    root,
    text="Weather Info",
    font=("Arial", 12, "bold")
)
result_label.pack(pady=5)

temp_label = tk.Label(root, text="Temperature: --")
temp_label.pack()

feels_label = tk.Label(root, text="Feels Like: --")
feels_label.pack()

humidity_label = tk.Label(root, text="Humidity: --")
humidity_label.pack()

wind_label = tk.Label(root, text="Wind Speed: --")
wind_label.pack()

pressure_label = tk.Label(root, text="Pressure: --")
pressure_label.pack()

root.mainloop()
