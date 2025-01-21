import requests
from bs4 import BeautifulSoup
import json
import subprocess
from datetime import datetime, timezone, timedelta

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
def update_log_file(timestamp, snow_temp, air_temp, updated_time):
    # Försök läsa existerande loggdata
    try:
        with open(log_file, "r") as file:
            soup = BeautifulSoup(file, "html.parser")
            table = soup.find("table")
    except FileNotFoundError:
        # Om loggfilen inte finns, skapa en ny tabell
        soup = BeautifulSoup("", "html.parser")
        table = soup.new_tag("table", style="width: 90%; margin: 30px auto; border-collapse: collapse; background-color: #fafafa;")
        header_row = soup.new_tag("tr")
        headers = ["Tid", "Uppdaterad Tid", "Snötemp (°C)", "Lufttemp (°C)"]
        for header in headers:
            th = soup.new_tag("th", style="padding: 12px; background-color: #4CAF50; color: white; font-size: 1.2em; text-align: center;")
            th.string = header
            header_row.append(th)
        table.append(header_row)

    # Lägg till en ny rad med data före de befintliga raderna
    new_row = soup.new_tag("tr", style="text-align: center;")
    time_cell = soup.new_tag("td", style="padding: 8px 15px; border: 1px solid #ddd;")
    time_cell.string = timestamp
    updated_time_cell = soup.new_tag("td", style="padding: 8px 15px; border: 1px solid #ddd;")
    updated_time_cell.string = updated_time
    snow_cell = soup.new_tag("td", style="padding: 8px 15px; border: 1px solid #ddd;")
    snow_cell.string = str(snow_temp)
    air_cell = soup.new_tag("td", style="padding: 8px 15px; border: 1px solid #ddd;")
    air_cell.string = str(air_temp)
    new_row.append(time_cell)
    new_row.append(updated_time_cell)
    new_row.append(snow_cell)
    new_row.append(air_cell)

    # Lägg till den nya raden som den första raden
    table.insert(1, new_row)

    # Begränsa till senaste 3 timmars data (om mer än 91 rader, ta bort den äldsta)
    rows = table.find_all("tr")
    if len(rows) > 91:  # 91 rader = 1 rad för headers + 90 loggade timmar
        rows[-1].extract()  # Ta bort den äldsta raden (sist i tabellen)

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

# Funktion för att hämta svensk tid
def get_swedish_time():
    now = datetime.now()
    if now.month in [3, 4, 5, 6, 7, 8, 9, 10]:  # Sommartid (mellan mars och oktober)
        return datetime.now(timezone(timedelta(hours=2))).strftime("%H:%M:%S")
    else:  # Vintertid (mellan november och februari)
        return datetime.now(timezone(timedelta(hours=1))).strftime("%H:%M:%S")

# Huvudlogik för att hämta och processa data
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

    # Hämtar den aktuella tiden i svensk tid (UTC +1/2, beroende på sommar/vintertid)
    current_time = get_swedish_time()  # Tid i formatet HH:MM:SS

    # Uppdatera loggfilen med svensk tid
    update_log_file(current_time, snow_temp, air_temp, updated_time)

    # Uppdatera HTML-sidan
    snow_temp_color = get_temperature_color(snow_temp)
    air_temp_color = get_temperature_color(air_temp)

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Temperatur Logg vid Lindbäcksstadion</title>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                background-color: #f0f0f0;
                color: #333333;
                margin: 0;
                padding: 0;
                text-align: center;
            }}
            h1 {{
                background-color: #4CAF50;
                color: white;
                padding: 15px;
                font-size: 2.5em;
            }}
            table {{
                width: 80%;
                margin: 30px auto;
                border-collapse: collapse;
                background-color: #fafafa;
            }}
            th, td {{
                padding: 12px;
                text-align: center;
                border: 1px solid #ddd;
            }}
            th {{
                background-color: #4CAF50;
                color: white;
                font-size: 1.2em;
            }}
            tr:nth-child(even) {{
                background-color: #f9f9f9;
            }}
            tr:hover {{
                background-color: #f1f1f1;
            }}
        </style>
    </head>
    <body>
        <h1>Temperatur Logg vid Lindbäcksstadion</h1>
        <table>
            <tr>
                <th>Tid</th>
                <th>Uppdaterad Tid</th>
                <th>Snötemp (°C)</th>
                <th>Lufttemp (°C)</th>
            </tr>
    """
    
    # Lägg till loggdata till tabellen
    with open(log_file, "r") as file:
        soup = BeautifulSoup(file, "html.parser")
        rows = soup.find_all("tr")[1:]  # Hoppa över headerraden
        for row in rows:
            html_content += str(row)

    html_content += """
        </table>
    </body>
    </html>
    """

    # Skriv till temperature_log.html
    with open(log_file, "w") as file:
        file.write(html_content)

    write_new_data(snow_temp, air_temp)
    print("Loggfilen och data uppdaterades.")

    # Push till GitHub
    subprocess.run(["git", "add", "temperature_log.html", data_file])
    subprocess.run(["git", "commit", "-m", "Uppdaterad temperature_log.html med svensk tid"])
    subprocess.run(["git", "push"])

else:
    print(f"Kunde inte hämta data: {response.status_code}")
