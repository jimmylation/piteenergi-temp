import requests
from bs4 import BeautifulSoup
import json
import subprocess

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
    print("Data hämtades framgångsrikt!")
    soup = BeautifulSoup(response.text, 'html.parser')

    updated_time = soup.find(id="updated-time").text
    snow_temp = int(soup.find(id="snow-temp").text.replace("°", ""))
    air_temp = int(soup.find(id="air-temp").text.replace("°", ""))

    print(f"Uppdaterad tid: {updated_time}")
    print(f"Snötemp: {snow_temp}")
    print(f"Lufttemp: {air_temp}")

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
        <title>Välkommen till Lindbäcksstadion!</title>
        <style>
            body {{
                margin: 0;
                padding: 0;
                height: 100vh;
                width: 100vw;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                align-items: center;
                background: url('background.jpg') no-repeat center center fixed;
                background-size: cover;
                font-family: 'Arial', sans-serif;
                color: #ffffff;
                text-align: center;
            }}
            .header {{
                margin-top: 18px;
                font-size: 3rem;
                font-weight: bold;
                text-shadow: 2px 2px 4px #000000;
            }}
            .temperature-container {{
                flex: 1;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
            }}
            .temperature {{
                font-size: 14rem;
                font-weight: bold;
                color: #000099;
                text-shadow: 1px 1px 2px #000000, 2px 2px 4px #000000, -1px -1px 2px #000000;
                margin: 0;
            }}
            .source {{
                font-size: 1rem;
                margin-bottom: 20px;
                text-shadow: 1px 1px 3px #000000;
                background: rgba(0, 0, 0, 0.5);
                padding: 10px 20px;
                border-radius: 10px;
            }}
            .clock {{
                font-size: 1.2rem;
                color: #FFFFFF;
                margin-top: 10px;
                font-weight: bold;
                text-shadow: 1px 1px 3px #000000;
            }}
        </style>
    </head>
    <body>
        <div class="header">Välkommen till Lindbäcksstadion!</div>
        <div class="temperature-container">
            <div id="temperature" class="temperature">
                Snö: {snow_temp}° | Luft: {air_temp}°
            </div>
            <div id="clock" class="clock">Senast uppdaterad: {updated_time}</div>
        </div>
        <div class="source">
            Temperaturdata hämtad från <a href="https://temperatur.nu" target="_blank">Temperatur.nu</a>
        </div>
    </body>
    </html>
    """

    with open("index.html", "w") as file:
        file.write(html_content)

    write_new_data(snow_temp, air_temp)
    print("HTML och data uppdaterade.")

    # Push to GitHub
    subprocess.run(["git", "add", "index.html"])
    subprocess.run(["git", "commit", "-m", "Uppdaterad index.html"])
    subprocess.run(["git", "push"])
else:
    print(f"Kunde inte hämta data: {response.status_code}")
