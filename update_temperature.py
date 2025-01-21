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
            transition: opacity 0.5s ease-in-out;
        }}
        .snow-temp {{ color: {snow_temp_color}; }}
        .air-temp {{ color: {air_temp_color}; }}
        .clock {{
            font-size: 15rem;
            font-weight: bold;
            color: #FFFFFF;
            text-shadow: 1px 1px 2px #000000, 2px 2px 4px #000000, -1px -1px 2px #000000;
            margin: 0;
            opacity: 0;
            transition: opacity 0.5s ease-in-out;
        }}
        .update-time {{
            font-size: 1.2rem;
            color: #4A90E2;
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
            <br>
            <span class="update-time">Senast uppdaterad: {updated_time}</span>
        </div>
        <div id="bigClock" class="clock">{updated_time.split(" ")[1]}</div>
    </div>
    <div class="source">
        Kontrolldata från Temperatur.nu: 
        <script type="text/javascript" src="https://www.temperatur.nu/jstemp.php?s=pitea-lindbacksstadion"></script>
    </div>

    <script>
        let temperature = document.getElementById("temperature");
        let bigClock = document.getElementById("bigClock");

        function toggleDisplay() {{
            if (temperature.style.opacity == 1 || temperature.style.opacity === "") {{
                temperature.style.opacity = 0;
                bigClock.style.opacity = 1;
            }} else {{
                temperature.style.opacity = 1;
                bigClock.style.opacity = 0;
            }}
        }}

        // Visa temperatur i 5 sekunder, klocka i 3 sekunder
        setInterval(toggleDisplay, 8000);
    </script>
</body>
</html>
"""
