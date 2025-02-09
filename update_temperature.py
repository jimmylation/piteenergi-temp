import requests
from bs4 import BeautifulSoup
import json
import subprocess

url = "https://www.piteenergi.se/snotemperatur/"
data_file = "temperature_data.json"

proxies = {
    "http": "http://24.49.117.86:80",
    "https": "http://24.49.117.86:80"
}

def read_previous_data():
    try:
        with open(data_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"snow_temp": None, "air_temp": None}

def write_new_data(snow_temp, air_temp):
    with open(data_file, "w") as file:
        json.dump({"snow_temp": snow_temp, "air_temp": air_temp}, file)

def get_temperature_color(temperature):
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

response = requests.get(url, proxies=proxies)
if response.status_code == 200:
    print("Data hämtades framgångsrikt!")
    soup = BeautifulSoup(response.text, 'html.parser')
    
    snow_card = soup.find('div', {'data-id': 'e62e4e60-5774-11ec-868f-ab20b6d69604'})
    
    if snow_card:
        snow_temp_element = snow_card.find('div', {'class': 'm-snow-card__temp-sensor-value'})
        snow_temp = int(snow_temp_element.text.strip().replace("°", "")) if snow_temp_element else "Ej tillgänglig"
        
        air_temp_element = snow_card.find_all('div', {'class': 'm-snow-card__temp-sensor-value'})[1]
        air_temp = int(air_temp_element.text.strip().replace("°", "")) if air_temp_element else "Ej tillgänglig"
        
        update_time_element = snow_card.find('div', {'class': 'm-snow-card__temp-time'})
        updated_time = update_time_element.text.strip() if update_time_element else "Ej tillgänglig"
        
        print(f"Uppdaterad tid: {updated_time}")
        print(f"Snötemp: {snow_temp}")
        print(f"Lufttemp: {air_temp}")
        
        write_new_data(snow_temp, air_temp)
        print("Data uppdaterad.")
    else:
        print("Kunde inte hitta temperaturdata.")
else:
    print(f"Kunde inte hämta data: {response.status_code}")
