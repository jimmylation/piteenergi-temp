import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import pytz
import subprocess

url = "https://temperatur-lindbacksstadion.onrender.com/"
data_file = "temperature_log.json"
html_file = "temperature_log.html"
log_duration = timedelta(hours=3)  # Loggdata max tre timmar gammal

# Tidszon för Stockholm
local_tz = pytz.timezone("Europe/Stockholm")


def make_aware(dt):
    """Skapa tidszonsmedveten datetime."""
    return local_tz.localize(dt) if dt.tzinfo is None else dt


def read_log_data():
    """Läs loggdata från fil."""
    try:
        with open(data_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def write_log_data(log_data):
    """Skriv loggdata till fil."""
    with open(data_file, "w") as file:
        json.dump(log_data, file)


def create_log_html(log_data):
    """Generera HTML för loggdata."""
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Temperature Log</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f4f4f9;
                color: #333;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
            }}
            table {{
                border-collapse: collapse;
                width: 90%;
                max-width: 1000px;
                margin: 20px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: center;
            }}
            th {{
                background-color: #007BFF;
                color: white;
                font-weight: bold;
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
        <table>
            <thead>
                <tr>
                    <th>Faktisk Tid</th>
                    <th>Hämtad Tid</th>
                    <th>Snötemperatur (°C)</th>
                    <th>Lufttemperatur (°C)</th>
                    <th>Trend (Senaste Timme)</th>
                </tr>
            </thead>
            <tbody>
    """

    for entry in log_data:
        html_content += f"""
        <tr>
            <td>{entry['actual_time']}</td>
            <td>{entry['retrieved_time']}</td>
            <td>{entry['snow_temp']}</td>
            <td>{entry['air_temp']}</td>
            <td>{entry.get('trend', 'Ingen trend')}</td>
        </tr>
        """

    html_content += """
            </tbody>
        </table>
    </body>
    </html>
    """

    with open(html_file, "w") as file:
        file.write(html_content)


def fetch_temperature():
    """Hämta temperaturdata från server."""
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        updated_time = soup.find(id="updated-time").text
        snow_temp = int(soup.find(id="snow-temp").text.replace("°", ""))
        air_temp = int(soup.find(id="air-temp").text.replace("°", ""))
        return updated_time, snow_temp, air_temp
    else:
        raise Exception(f"Failed to fetch data: {response.status_code}")


def calculate_trend(log_data):
    """Beräkna trend för den senaste timmen."""
    if len(log_data) < 2:
        return "Ingen trend"

    recent_entries = [
        entry for entry in log_data if make_aware(datetime.strptime(entry["actual_time"], "%Y-%m-%d %H:%M:%S"))
        > make_aware(datetime.now()) - timedelta(hours=1)
    ]

    if len(recent_entries) < 2:
        return "Ingen trend"

    first_temp = recent_entries[0]
    last_temp = recent_entries[-1]

    if last_temp['snow_temp'] > first_temp['snow_temp']:
        return "Stigande"
    elif last_temp['snow_temp'] < first_temp['snow_temp']:
        return "Fallande"
    else:
        return "Oförändrad"


def log_temperature():
    """Hämta, logga och publicera temperaturdata."""
    try:
        retrieved_time, snow_temp, air_temp = fetch_temperature()

        actual_time = make_aware(datetime.now()).strftime("%Y-%m-%d %H:%M:%S")

        log_data = read_log_data()

        if not log_data or log_data[0]["retrieved_time"] != retrieved_time:
            log_data.insert(0, {
                "actual_time": actual_time,
                "retrieved_time": retrieved_time,
                "snow_temp": snow_temp,
                "air_temp": air_temp
            })

        trend = calculate_trend(log_data)
        log_data[0]["trend"] = trend

        cutoff_time = make_aware(datetime.now()) - log_duration
        log_data = [entry for entry in log_data if make_aware(datetime.strptime(entry["actual_time"], "%Y-%m-%d %H:%M:%S")) >= cutoff_time]

        write_log_data(log_data)
        create_log_html(log_data)

        # Push ändringarna till GitHub
        subprocess.run(["git", "config", "--global", "user.name", "GitHub Actions Bot"])
        subprocess.run(["git", "config", "--global", "user.email", "actions@github.com"])
        subprocess.run(["git", "add", html_file])
        subprocess.run(["git", "commit", "-m", "Uppdaterad temperature_log.html med trend"])
        subprocess.run(["git", "push", "https://x-access-token:${GH_TOKEN}@github.com/${{ github.repository }}", "HEAD:main"])
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    log_temperature()
