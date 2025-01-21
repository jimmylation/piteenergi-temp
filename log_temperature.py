import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
import os

# URL till temperaturdatakällan
url = "https://temperatur-lindbacksstadion.onrender.com/"
data_file = "temperature_log.json"
html_file = "temperature_log.html"

# Läs tidigare loggad data
def read_previous_data():
    if os.path.exists(data_file):
        with open(data_file, "r") as file:
            return json.load(file)
    else:
        return []

# Skriv ny loggdata till JSON-fil
def write_new_data(log_data):
    with open(data_file, "w") as file:
        json.dump(log_data, file)

# Beräkna trend baserat på senaste timmens data
def calculate_trend(temps):
    if len(temps) < 2:
        return "Ingen trend"
    
    # Här antas att varje element är en ordbok med nyckeln 'snow_temp' eller 'air_temp'
    change = temps[-1]['snow_temp'] - temps[0]['snow_temp']  # För snötemp
    if change > 0:
        return "Uppåt"
    elif change < 0:
        return "Nedåt"
    else:
        return "Oförändrat"
    
    # Beräkna förändring över senaste 60 minuterna
    change = temps[-1][1] - temps[0][1]  # temp[-1][1] betyder den senaste temperaturen
    if change > 0:
        return "Uppåt"
    elif change < 0:
        return "Nedåt"
    else:
        return "Oförändrat"

# Hämta temperatur och uppdaterad tid
def get_temperatures():
    response = requests.get(url)
    if response.status_code == 200:
        print("Data hämtades framgångsrikt!")
        soup = BeautifulSoup(response.text, 'html.parser')

        updated_time = soup.find(id="updated-time").text.strip()
        snow_temp = int(soup.find(id="snow-temp").text.replace("°", "").strip())
        air_temp = int(soup.find(id="air-temp").text.replace("°", "").strip())

        return updated_time, snow_temp, air_temp
    else:
        print(f"Kunde inte hämta data: {response.status_code}")
        return None, None, None

# Skapa HTML-tabell
def create_html_table(log_data):
    table_rows = ""
    for entry in log_data:
        table_rows += f"""
        <tr>
            <td>{entry['timestamp']}</td>
            <td>{entry['updated_time']}</td>
            <td>{entry['snow_temp']}°C</td>
            <td>{entry['snow_trend']}</td>
            <td>{entry['air_temp']}°C</td>
            <td>{entry['air_trend']}</td>
        </tr>
        """
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Temperatur Logg</title>
        <style>
            table {{
                width: 100%;
                border-collapse: collapse;
            }}
            th, td {{
                padding: 10px;
                border: 1px solid #ddd;
                text-align: center;
            }}
            th {{
                background-color: #f2f2f2;
            }}
        </style>
    </head>
    <body>
        <h1>Temperatur Logg</h1>
        <table>
            <thead>
                <tr>
                    <th>Klockslag hämtad</th>
                    <th>Tid uppdaterad</th>
                    <th>Snötemp</th>
                    <th>Trend snötemp</th>
                    <th>Lufttemp</th>
                    <th>Trend lufttemp</th>
                </tr>
            </thead>
            <tbody>
                {table_rows}
            </tbody>
        </table>
    </body>
    </html>
    """

    with open(html_file, "w") as file:
        file.write(html_content)
    print(f"HTML-tabell skapad: {html_file}")

# Kör programmet varje minut under tre timmar
def log_temperature():
    log_data = read_previous_data()
    
    for _ in range(180):  # 180 iterationer för att köra i tre timmar
        updated_time, snow_temp, air_temp = get_temperatures()
        if updated_time is not None:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Filtrera de senaste temperaturvärdena från log_data
            snow_temps = [entry for entry in log_data if entry['snow_temp'] is not None]
            air_temps = [entry for entry in log_data if entry['air_temp'] is not None]
            
            snow_trend = calculate_trend(snow_temps)  # Skicka listan av snötemperaturer
            air_trend = calculate_trend(air_temps)    # Skicka listan av lufttemperaturer

            log_data.insert(0, {
                'timestamp': timestamp,
                'updated_time': updated_time,
                'snow_temp': snow_temp,
                'snow_trend': snow_trend,
                'air_temp': air_temp,
                'air_trend': air_trend
            })

            # Begränsa loggdatamängden till de senaste 60 minuterna (ungefär)
            log_data = log_data[:60]
            
            write_new_data(log_data)
            create_html_table(log_data)

        time.sleep(60)  # Vänta en minut innan nästa iteration

if __name__ == "__main__":
    log_temperature()
