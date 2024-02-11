import io

import requests
from PIL import ImageTk, Image
import tkinter as tk
import sys

def style_gui(window):
    window.title("GeoTraceExplorer")
    window.configure(bg="white")
    label_font = ("Arial", 12, "bold")

    # Configure the labels
    latitude_label.configure(font=label_font)
    latitude_label.pack()

    longitude_label.configure(font=label_font)
    longitude_label.pack()

    location_label.configure(font=label_font)
    location_label.pack()

    latitude_entry.configure(font=label_font)
    latitude_entry.pack()

    longitude_entry.configure(font=label_font)
    longitude_entry.pack()

    get_location_button.configure(font=label_font)
    get_location_button.pack(pady=10)

    stop_button.configure(font=label_font)
    stop_button.pack()

def get_nominatim_location():
    latitude = float(latitude_entry.get())
    longitude = float(longitude_entry.get())

    url = f"https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat={latitude}&lon={longitude}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        address = data.get('display_name')
        if address:
            location_label.config(text="Location: " + address)
            map_image_url = f"https://maps.openstreetmap.org/?mlat={latitude}&mlon={longitude}&zoom=12&width=400&height=400"
            show_map_image(address, map_image_url)
        else:
            location_label.config(text="Address not found.")
    else:
        location_label.config(text="Error occurred: " + str(response.status_code))

def get_weather_report():
    latitude = float(latitude_entry.get())
    longitude = float(longitude_entry.get())
    weather_data = retrieve_weather_report(latitude, longitude)
    if weather_data:
        temperature = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        description = weather_data['weather'][0]['description']
        weather_report = f"Temperature: {temperature}°C\n"
        weather_report += f"Humidity: {humidity}%\n"
        weather_report += f"Description: {description}"

        weather_label.config(text=weather_report)
    else:
         weather_label.config(text="Failed to retrieve weather report.")

def retrieve_weather_report(latitude, longitude):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid='521b72f9970c3c7146e15b6d476ea0eb'"

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def show_weather_report(weather_data):
    temperature = weather_data['main']['temp']
    humidity = weather_data['main']['humidity']
    description = weather_data['weather'][0]['description']

    report_window = tk.Toplevel()
    report_window.title("Weather Report")

    temperature_label = tk.Label(report_window, text=f"Temperature: {temperature}°C")
    temperature_label.pack()
    humidity_label = tk.Label(report_window, text=f"Humidity: {humidity}%")
    humidity_label.pack()
    description_label = tk.Label(report_window, text=f"Description: {description}")
    description_label.pack()

def show_map_image(address, map_image_url):
    window = tk.Toplevel()
    window.title("Map Image")

    response = requests.get(map_image_url)
    print("Status code:", response.status_code)
    if response.status_code == 200:
        image_data = response.content
        try:
            image = Image.open(io.BytesIO(image_data))
        except Exception as e:
            print("Error opening image:", e)
        image = image.resize((50, 50), Image.ANTIALIAS)
        image_tk = ImageTk.PhotoImage(image)
        image_label = tk.Label(window, image=image_tk)
        image_label.image = image_tk
        image_label.pack()

        address_label = tk.Label(window, text=address)
        address_label.pack()
    else:
        error_label = tk.Label(window, text="Failed to retrieve the map image.")
        error_label.pack()

def get_soil_statistics():
    latitude = float(latitude_entry.get())
    longitude = float(longitude_entry.get())

    # API endpoint URL
    url = f"https://api.soilgrids.ca/query?lon={longitude}&lat={latitude}"

    # Make the request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        # Process the data as needed
        print(data)
    else:
        print("Error:", response.status_code)


def stop_program():
    sys.exit(0)
    pass



window = tk.Tk()
window.title("GeoTraceExplorer")
latitude_label = tk.Label(window, text="Latitude:")
latitude_label.pack()
latitude_entry = tk.Entry(window)
latitude_entry.pack()
longitude_label = tk.Label(window, text="Longitude:")
longitude_label.pack()
longitude_entry = tk.Entry(window)
longitude_entry.pack()
location_label = tk.Label(window, text="Location:")
location_label.pack()
get_weather_button = tk.Button(window, text="Get Weather", command=get_weather_report)
get_weather_button.pack()

weather_label = tk.Label(window)
weather_label.pack()
get_location_button = tk.Button(window, text="Get Location", command=get_nominatim_location)
#button = tk.Button(window, text="Get Location", command=get_nominatim_location)
stop_button = tk.Button(window, text="stop", command=stop_program)
#button.pack()
button = tk.Button(window, text="Get Soil Statistics", command=get_soil_statistics)
button.pack()
stop_button.pack()

style_gui(window)
window.mainloop()


