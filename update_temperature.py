import requests
from bs4 import BeautifulSoup
import json
import subprocess
import os
import time
from datetime import datetime

url = "https://temperatur-lindbacksstadion.onrender.com/"
data_file = "temperature_data.json"
log_file = "temperature_log.html"

def read_previous_data():
    try:
        with open(data_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"snow_temp": None, "air_temp": None, "last_updated_time": None}

def write_new_data(snow_temp, air_temp, updated_time):
    with open(data_file, "w") as file:
        json.dump({"snow_temp": snow_temp, "air_temp": air_temp, "last_updated_time": updated_time}, file)

def get_temperature_color(temperature):
    if temperature > 1:
        return "#FF0000"  # Röd
    elif 1 >= temperature >= -4:
        return "#8A2BE2"  # Violett
    elif -4 > temperature >= -10:
        return "#0000FF"  # Blå
    elif -10 > temperature >= -20:
        return "#006400"  # Grön
    else:
        return "#FFFFFF"  # Vit

def log_temperature(snow_temp, air_temp, updated_time):
    # Läs in gamla loggar
    if os.path.exists(log_file):
        with open(log_file, "r") as file:
            log_data = file.read()
    else:
        log_data = ""

    # Skapa en ny loggpost
    new_log_entry = f"""
        <tr>
            <td>{updated_time}</td>
            <td>{snow_temp}°C</td>
            <td>{air_temp}°C</td>
        </tr>
    """

    # Lägg till den nya loggposten
    log_data = log_data.replace("</table>", new_log_entry + "</table>")

    # Skriv tillbaka den uppdaterade loggen till HTML-filen
    with open(log_file, "w") as file:
        if log_data.strip() == "":
            file.write(f"""
                <!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Temperaturlogg</title>
                    <style>
                        table {{
                            width: 100%;
                            border-collapse: collapse;
                            margin: 20px 0;
                        }}
                        th, td {{
                            padding: 8px 12px;
                            border: 1px solid #ddd;
                            text-align: center;
                        }}
                        th {{
                            background-color: #4CAF50;
                            color: white;
                        }}
                        tr:nth-child(even) {{
                            background-color: #f2f2f2;
                        }}
                        tr:hover {{
                            background-color: #ddd;
                        }}
                    </style>
                </head>
                <body>
                    <h2>Temperaturlogg (Senaste 3 timmarna)</h2>
                    <table>
                        <tr>
                            <th>Tid</th>
                            <th>Snötemp</th>
                            <th>Lufttemp</th>
                        </tr>
                        {new_log_entry}
                    </table>
                </body>
                </html>
            """)
        else:
            file.write(log_data)

def main():
    previous_data = read_previous_data()
    previous_snow_temp = previous_data["snow_temp"]
    previous_air_temp = previous_data["air_temp"]
    previous_updated_time = previous_data["last_updated_time"]

    while True:
        response = requests.get(url)
        if response.status_code == 200:
            print("Data hämtades framgångsrikt!")
            soup = BeautifulSoup(response.text, 'html.parser')

            updated_time = soup.find(id="updated-time").text.strip()
            snow_temp = int(soup.find(id="snow-temp").text.replace("°", ""))
            air_temp = int(soup.find(id="air-temp").text.replace("°", ""))

            print(f"Uppdaterad tid: {updated_time}")
            print(f"Snötemp: {snow_temp}")
            print(f"Lufttemp: {air_temp}")

            # Logga enbart om tiden har ändrats
            if updated_time != previous_updated_time:
                snow_temp_color = get_temperature_color(snow_temp)
                air_temp_color = get_temperature_color(air_temp)
                
                # Logga temperaturerna
                log_temperature(snow_temp, air_temp, updated_time)

                # Spara de nya temperaturerna och senaste uppdaterade tid
                write_new_data(snow_temp, air_temp, updated_time)

                # Uppdatera för nästa iteration
                previous_updated_time = updated_time

        else:
            print(f"Kunde inte hämta data: {response.status_code}")
        
        # Vänta en minut innan nästa kontroll
        time.sleep(60)

if __name__ == "__main__":
    main()
