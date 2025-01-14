import requests
from bs4 import BeautifulSoup
import json

url = "https://temperatur-lindbacksstadion.onrender.com/"
data_file = "temperature_data.json"

def read_previous_data():
    try:
        with open(data_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"snow_temp": None, "air_temp": None}

def write_new_data(snow_temp, air_temp):
    with open(data_file, "w") as file:
        json.dump({"snow_temp": snow_temp, "air_temp": air_temp}, file)

response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    updated_time = soup.find(id="updated-time").text
    snow_temp = int(soup.find(id="snow-temp").text.replace("°", ""))
    air_temp = int(soup.find(id="air-temp").text.replace("°", ""))

    previous_data = read_previous_data()
    previous_snow_temp = previous_data["snow_temp"]
    previous_air_temp = previous_data["air_temp"]

    snow_trend = "neutral" if previous_snow_temp is None else "up" if snow_temp > previous_snow_temp else "down"
    air_trend = "neutral" if previous_air_temp is None else "up" if air_temp > previous_air_temp else "down"

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Temperaturtrender</title>
        <style>
            .trend-up {{ color: red; }}
            .trend-down {{ color: blue; }}
        </style>
    </head>
    <body>
        <h1>Temperaturtrender vid Lindbäcksstadion</h1>
        <p>Senast uppdaterad: {updated_time}</p>
        <p>Snötemp: {snow_temp}° <span class="trend-{snow_trend}">{"↑" if snow_trend == "up" else "↓" if snow_trend == "down" else ""}</span></p>
        <p>Lufttemp: {air_temp}° <span class="trend-{air_trend}">{"↑" if air_trend == "up" else "↓" if air_trend == "down" else ""}</span></p>
    </body>
    </html>
    """

    with open("index.html", "w") as file:
        file.write(html_content)

    write_new_data(snow_temp, air_temp)
    print("HTML och data uppdaterade.")
else:
    print("Kunde inte hämta data:", response.status_code)
