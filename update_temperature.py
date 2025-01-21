import requests
from bs4 import BeautifulSoup
import json
import subprocess
from datetime import datetime
import time

url = "https://temperatur-lindbacksstadion.onrender.com/"
data_file = "temperature_data.json"
log_file = "temperature_log.html"

# Läs tidigare temperaturdata
def read_previous_data():
    try:
        with open(data_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"snow_temp": None, "air_temp": None}

# Skriv nya temperaturdata
def write_new_data(snow_temp, air_temp):
    with open(data_file, "w") as file:
        json.dump({"snow_temp": snow_temp, "air_temp": air_temp}, file)

# Uppdatera loggfilen
def update_log_file(timestamp, snow_temp, air_temp):
    # Försök läsa existerande loggdata
    try:
        with open(log_file, "r") as file:
            soup = BeautifulSoup(file, "html.parser")
            table = soup.find("table")
    except FileNotFoundError:
        # Om loggfilen inte finns, skapa en ny tabell
        soup = BeautifulSoup("", "html.parser")
        table = soup.new_tag("table", border="1", style="width: 100%; text-align: center; border-collapse: collapse;")
        header_row = soup.new_tag("tr")
        headers = ["Tid", "Snötemp (°C)", "Lufttemp (°C)"]
        for header in headers:
            th = soup.new_tag("th")
            th.string = header
            header_row.append(th)
        table.append(header_row)

    # Lägg till en ny rad med data
    new_row = soup.new_tag("tr")
    time_cell = soup.new_tag("td")
    time_cell.string = timestamp
    snow_cell = soup.new_tag("td")
    snow_cell.string = str(snow_temp)
    air_cell = soup.new_tag("td")
    air_cell.string = str(air_temp)
    new_row.append(time_cell)
    new_row.append(snow_cell)
    new_row.append(air_cell)
    table.append(new_row)

    # Begränsa till senaste 3 timmars data (om mer än 12 rader, ta bort den äldsta)
    rows = table.find_all("tr")
    if len(rows) > 13:  # 13 rader = 1 rad för headers + 12 loggade timmar (3 timmar)
        rows[1].extract()

    # Spara tabellen i loggfilen
    soup.clear()
    soup.append(table)
    with open(log_file, "w") as file:
        file.write(str(soup))

# Hämta färg för temperatur
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

# Huvudlogik för att hämta och processa data
def log_temperature_data():
    # Variabel för senaste loggade tid
    last_logged_time = None

    while True:
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

            # Kontrollera om vi har en ny tid
            if updated_time != last_logged_time:
                # Om tiden är ny, logga data
                current_time = datetime.now().strftime("%H:%M:%S")
                update_log_file(current_time, snow_temp, air_temp)

                # Uppdatera senaste loggade tid
                last_logged_time = updated_time

                # Skriv nya temperaturdata
                write_new_data(snow_temp, air_temp)
                print(f"Temperaturer loggade vid: {current_time}")

            # Vänta en minut innan nästa koll
            time.sleep(60)

        else:
            print(f"Kunde inte hämta data: {response.status_code}")
            # Vänta en minut innan nästa försök
            time.sleep(60)

# Starta loggning
log_temperature_data()
