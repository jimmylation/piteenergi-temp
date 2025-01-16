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
        a {{
            color: #ffffff;
            text-decoration: none;
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
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .snow-temp {{ color: {snow_temp_color}; }}
        .air-temp {{ color: {air_temp_color}; }}
        .trend-arrow {{
            font-size: 5rem;
            margin-left: 15px;
            position: relative;
            top: 0.1em;
        }}
        .trend-up {{ color: red; }}
        .trend-down {{ color: blue; }}
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
    </style>
</head>
<body>
    <div class="header">Välkommen till Lindbäcksstadion!</div>
    <div class="temperature-container">
        <div id="temperature" class="temperature">
            <span class="snow snow-temp">Snön {snow_temp}°C</span>
            <span class="trend-arrow {snow_trend_class}">{'↑' if snow_trend == 'up' else '↓'}</span>
        </div>
        <div id="temperature" class="temperature">
            <span class="air air-temp">Luften {air_temp}°C</span>
            <span class="trend-arrow {air_trend_class}">{'↑' if air_trend == 'up' else '↓'}</span>
        </div>
        <div id="clock" class="clock">Senast uppdaterad: {updated_time}</div>
    </div>
    <div class="source">
        Kontrolldata från <a href="https://www.temperatur.nu">Temperatur.nu</a>: 
        <script type="text/javascript" src="https://www.temperatur.nu/jstemp.php?s=pitea-lindbacksstadion"></script>
    </div>
</body>
</html>
"""
