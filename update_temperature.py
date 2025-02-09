import requests
from bs4 import BeautifulSoup
import json
import subprocess

# Lista över proxys i formatet {"http": "IP:port", "https": "IP:port"}
proxies_list = [
    {"http": "http://24.49.117.86:80", "https": "http://24.49.117.86:80"},
    {"http": "http://3.130.65.162:3128", "https": "http://3.130.65.162:3128"},
    {"http": "http://64.147.212.78:8080", "https": "http://64.147.212.78:8080"},
    {"http": "http://31.40.248.2:8080", "https": "http://31.40.248.2:8080"},
    {"http": "http://13.37.89.201:80", "https": "http://13.37.89.201:80"},
    {"http": "http://13.37.59.99:3128", "https": "http://13.37.59.99:3128"},
]

# URL till sidan vi vill hämta
url = "https://www.piteenergi.se/snotemperatur/"
data_file = "temperature_data.json"

def find_working_proxy():
    """Testar proxys en och en tills en fungerar."""
    for proxy in proxies_list:
        try:
            print(f"🔄 Testar proxy: {proxy['http']}")
            response = requests.get(url, proxies=proxy, timeout=5)  # Timeout efter 5 sekunder
            if response.status_code == 200:
                print(f"✅ Proxy fungerar: {proxy['http']}")
                return proxy  # Returnerar fungerande proxy
        except requests.RequestException:
            print(f"❌ Proxy misslyckades: {proxy['http']}")
    
    print("🚨 Ingen proxy fungerade!")
    return None

def read_previous_data():
    """Läser tidigare sparad temperaturdata."""
    try:
        with open(data_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"snow_temp": None, "air_temp": None}

def write_new_data(snow_temp, air_temp):
    """Sparar ny temperaturdata i JSON-fil."""
    with open(data_file, "w") as file:
        json.dump({"snow_temp": snow_temp, "air_temp": air_temp}, file)

def get_temperature_color(temperature):
    """Returnerar färg baserat på temperatur."""
    if temperature > 1:
        return "#FF6666"  # Röd
    elif 1 >= temperature >= -4:
        return "#AC64E9"  # Violett
    elif -4 > temperature >= -10:
        return "#6666FF"  # Blå
    elif -10 > temperature >= -20:
        return "#57D957"  # Grön
    else:
        return "#FFFFFF"  # Vit

# Hitta en fungerande proxy
working_proxy = find_working_proxy()

if working_proxy:
    # Hämta sidan med fungerande proxy
    response = requests.get(url, proxies=working_proxy)
    
    if response.status_code == 200:
        print("✅ Data hämtades framgångsrikt!")
        soup = BeautifulSoup(response.text, 'html.parser')

        updated_time = soup.find(id="updated-time").text
        snow_temp = int(soup.find(id="snow-temp").text.replace("°", ""))
        air_temp = int(soup.find(id="air-temp").text.replace("°", ""))

        print(f"📅 Uppdaterad tid: {updated_time}")
        print(f"❄️ Snötemp: {snow_temp}°C")
        print(f"🌬️ Lufttemp: {air_temp}°C")

        # Bestäm färger
        snow_temp_color = get_temperature_color(snow_temp)
        air_temp_color = get_temperature_color(air_temp)

        # HTML-innehåll
        html_content = f"""
        <!DOCTYPE html>
        <html lang="sv">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Temperatur vid Lindbäcksstadion</title>
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    height: 100vh;
                    width: 100vw;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    background: url('background.jpg') no-repeat center center fixed;
                    background-size: cover;
                    font-family: 'Arial', sans-serif;
                    color: #ffffff;
                    text-align: center;
                }}
                .temperature {{
                    font-size: 8rem;
                    font-weight: bold;
                    text-shadow: 2px 2px 4px #000000;
                }}
                .snow-temp {{ color: {snow_temp_color}; }}
                .air-temp {{ color: {air_temp_color}; }}
                .clock {{
                    font-size: 1.5rem;
                    font-weight: bold;
                    margin-top: 20px;
                }}
            </style>
        </head>
        <body>
            <h1>Välkommen till Lindbäcksstadion!</h1>
            <div class="temperature">
                <span class="snow-temp">Snön {snow_temp}°C</span>
                <br>
                <span class="air-temp">Luften {air_temp}°C</span>
            </div>
            <div class="clock">Senast uppdaterad: {updated_time}</div>
        </body>
        </html>
        """
        
        # Skriv till index.html
        with open("index.html", "w") as file:
            file.write(html_content)

        # Spara temperaturdata
        write_new_data(snow_temp, air_temp)
        print("✅ HTML och data uppdaterade.")

        # Push till GitHub
        subprocess.run(["git", "add", "index.html"])
        subprocess.run(["git", "commit", "-m", "Uppdaterad index.html"])
        subprocess.run(["git", "push"])
    else:
        print(f"❌ Kunde inte hämta data: {response.status_code}")
else:
    print("⚠️ Ingen fungerande proxy hittades.")
