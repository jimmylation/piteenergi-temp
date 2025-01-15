def get_temperature_color(temp):
    """Returnerar färg baserat på temperaturintervall."""
    if temp > 1:
        return "#FF6666"  # Nedtonat rött
    elif 1 >= temp > -4:
        return "#CC66FF"  # Nedtonat violett
    elif -4 >= temp > -10:
        return "#6699FF"  # Nedtonat blått
    elif -10 >= temp > -20:
        return "#66CC66"  # Nedtonat grönt
    else:
        return "#FFFFFF"  # Vitt

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
    
    # Hämta färger baserat på temperaturintervall
    snow_color = get_temperature_color(snow_temp)
    air_color = get_temperature_color(air_temp)
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Välkommen till Lindbäcksstadion!</title>
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
                flex: 1;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
            }}
            .temperature {{
                font-size: 10rem;
                font-weight: bold;
                margin: 0;
            }}
            .snow {{
                color: {snow_color};
                text-shadow: 1px 1px 2px #000000, 2px 2px 4px #000000, -1px -1px 2px #000000;
            }}
            .air {{
                color: {air_color};
                text-shadow: 1px 1px 2px #000000, 2px 2px 4px #000000, -1px -1px 2px #000000;
            }}
            .source {{
                font-size: 1rem;
                margin-bottom: 20px;
                text-shadow: 1px 1px 3px #000000;
                background: rgba(0, 0, 0, 0.5);
                padding: 10px 20px;
                border-radius: 10px;
            }}
            .source a {{
                text-decoration: none;
                color: #ffffff;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="header">Välkommen till Lindbäcksstadion!</div>
        <div class="temperature-container">
            <div id="temperature" class="temperature">
                <span class="snow">Snö: {snow_temp}°</span>
                <span class="air">Luft: {air_temp}°</span>
            </div>
            <div id="clock" class="clock">Senast uppdaterad: {updated_time}</div>
        </div>
        <div class="source">
            Kontrolldata från Temperatur.nu: 
            <script type="text/javascript" src="https://www.temperatur.nu/jstemp.php?s=pitea-lindbacksstadion"></script>
        </div>
    </body>
    </html>
    """
    
    with open("index.html", "w") as file:
        file.write(html_content)

    write_new_data(snow_temp, air_temp)
    print("HTML och data uppdaterade.")

    subprocess.run(["git", "add", "index.html"])
    subprocess.run(["git", "commit", "-m", "Uppdaterad index.html"])
    subprocess.run(["git", "push"])
else:
    print(f"Kunde inte hämta data: {response.status_code}")
