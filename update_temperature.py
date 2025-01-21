import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime, timedelta

# URL för att hämta data
url = "https://temperatur-lindbacksstadion.onrender.com/"
log_file = "temperature_log.html"
data_file = "temperature_data.json"

def read_previous_data():
    try:
        with open(data_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"snow_temp": None, "air_temp": None, "last_updated": None}

def write_new_data(snow_temp, air_temp, last_updated):
    with open(data_file, "w") as file:
        json.dump({"snow_temp": snow_temp, "air_temp": air_temp, "last_updated": last_updated}, file)

def log_temperature_data(current_time, snow_temp, air_temp):
    # Läs senaste loggade data
    previous_data = read_previous_data()

    # Logga data bara om tiden har uppdaterats (inte temperaturen)
    if current_time != previous_data["last_updated"]:
        # Lägg till en ny loggpost i HTML-fil
        with open(log_file, "a") as file:
            file.write(f"""
            <tr>
                <td>{current_time}</td>
                <td>{snow_temp}°C</td>
                <td>{air_temp}°C</td>
            </tr>
            """)

        # Uppdatera senaste loggade tid och temperaturer
        write_new_data(snow_temp, air_temp, current_time)
        print(f"Loggat ny temperaturdata vid: {current_time}")

def create_log_file_header():
    # Skapa filens header om den inte redan finns
    try:
        with open(log_file, "r") as file:
            return  # Filen finns redan, inget att göra
    except FileNotFoundError:
        with open(log_file, "w") as file:
            file.write("""
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Temperaturlogg</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f4f4f9; }
                    table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                    th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
                    th { background-color: #4CAF50; color: white; }
                    tr:hover { background-color: #f1f1f1; }
                    h1 { text-align: center; color: #333; font-size: 24px; }
                    .container { width: 80%; margin: 0 auto; }
                    footer { text-align: center; margin-top: 40px; font-size: 14px; color: #666; }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Temperaturlogg för Lindbäcksstadion</h1>
                    <table>
                        <tr>
                            <th>Tid</th>
                            <th>Snötemp</th>
                            <th>Lufttemp</th>
                        </tr>
            """)
            print("Skapade ny loggfil med header.")

def close_log_file():
    # Stäng taggarna för HTML-filen när loggningen är klar
    with open(log_file, "a") as file:
        file.write("""
                    </table>
                    <footer>
                        <p>Loggad data under de senaste tre timmarna</p>
                    </footer>
                </div>
            </body>
            </html>
            """)
    print("Loggfil stängd.")

def fetch_and_log_temperature():
    create_log_file_header()

    last_logged_time = None
    end_time = datetime.now() + timedelta(hours=3)  # Logga under tre timmar

    while datetime.now() < end_time:
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

            current_time = datetime.now().strftime("%H:%M:%S")

            # Logga om klockan har uppdaterats
            if updated_time != last_logged_time:
                log_temperature_data(current_time, snow_temp, air_temp)

                # Uppdatera senaste loggade tid
                last_logged_time = updated_time

            # Vänta 2 minuter innan nästa kontroll
            time.sleep(120)  # 2 minuter
        else:
            print(f"Kunde inte hämta data: {response.status_code}")
            time.sleep(60)  # Vänta en minut innan nästa försök

    close_log_file()
    print("Loggning avslutad efter 3 timmar.")

# Starta loggning
fetch_and_log_temperature()
