import requests
from bs4 import BeautifulSoup
import json
import subprocess
from datetime import datetime

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

    # Uppdatera loggfilen
    current_time = datetime.now().strftime("%H:%M:%S")
    update_log_file(current_time, snow_temp, air_temp)

    # Uppdatera HTML-sidan
    snow_temp_color = get_temperature_color(snow_temp)
    air_temp_color = get_temperature_color(air_temp)

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Temperaturtrender vid Lindbäcksstadion</title>
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
                position: relative;
                flex: 1;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                margin-top: 30px;
            }}
            .temperature {{
                font-size: 8rem;
                font-weight: bold;
                color: #000099;
                text-shadow: 1px 1px 2px #000000, 2px 2px 4px #000000, -1px -1px 2px #000000;
                margin: 0;
            }}
            .snow-temp {{ color: {snow_temp_color}; }}
            .air-temp {{ color: {air_temp_color}; }}
            .clock {{
                font-size: 1.2rem;
                color: #FFFFFF;
                margin-top: 10px;
                font-weight: bold;
                text-shadow: 1px 1px 3px #000000;
            }}
            .source {{
                font-size: 1rem;
                margin-bottom: 20px;
                text-shadow: 1px 1px 3px #000000;
                background: rgba(0, 0, 0, 0.5);
                padding: 10px 20px;
                border-radius: 10px;
            }}
            table {{
                width: 80%;
                margin: 20px 0;
                border-collapse: collapse;
                background-color: rgba(255, 255, 255, 0.8);
            }}
            th, td {{
                padding: 10px;
                border: 1px solid #ddd;
            }}
            th {{
                background-color: #4CAF50;
                color: white;
            }}
            tr:nth-child(even) {{
                background-color: #f2f2f2;
            }}
            a {{
                text-decoration: none;
                color: #FFFFFF;
            }}
        </style>
    </head>
    <body>
        <div class="header">Välkommen till Lindbäcksstadion!</div>
        <div class="temperature-container">
            <div id="temperature" class="temperature">
                <span class="snow snow-temp">Snön {snow_temp}°C</span>
                <br>
                <span class="air air-temp">Luften {air_temp}°C</span>
            </div>
            <div id="clock" class="clock">Senast uppdaterad: {updated_time}</div>
        </div>
        <div class="source">
            Kontrolldata från Temperatur.nu: 
            <script type="text/javascript" src="https://www.temperatur.nu/jstemp.php?s=pitea-lindbacksstadion"></script>
        </div>
        <div class="log-table">
            <h2>Temperatur Logg (Senaste 3 timmar)</h2>
            <table>
                <tr>
                    <th>Tid</th>
                    <th>Snötemp (°C)</th>
                    <th>Lufttemp (°C)</th>
                </tr>
                <!-- Här kommer tabellen med data -->
            </table>
        </div>
    </body>
    </html>
    """
    
    # Skriv till index.html
    with open("index.html", "w") as file:
        file.write(html_content)

    write_new_data(snow_temp, air_temp)
    print("HTML och data uppdaterade.")

    # Push till GitHub
    subprocess.run(["git", "add", "index.html", log_file])
    subprocess.run(["git", "commit", "-m", "Uppdaterad index.html och loggfil"])
    subprocess.run(["git", "push"])
else:
    print(f"Kunde inte hämta data: {response.status_code}")
