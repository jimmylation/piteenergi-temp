import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import pytz
import os
import subprocess

url = "https://temperatur-lindbacksstadion.onrender.com/"
data_file = "temperature_log.json"
html_file = "temperature_log.html"
log_duration = timedelta(hours=3)  # Loggdata max tre timmar gammal

# Tidszon för Stockholm
local_tz = pytz.timezone("Europe/Stockholm")

# Funktion för att skapa tidszonsmedvetna datetime
def make_aware(dt):
    return local_tz.localize(dt) if dt.tzinfo is None else dt

def read_log_data():
    try:
        with open(data_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def write_log_data(log_data):
    with open(data_file, "w") as file:
        json.dump(log_data, file)

def create_log_html(log_data):
    # Generera HTML med logg
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
                background-color: #f4f4f9
