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
        .temperature-row {{
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 20px 0;
        }}
        .snow-temp {{ color: {get_temperature_color(snow_temp)}; }}
        .air-temp {{ color: {get_temperature_color(air_temp)}; }}
        .trend-arrow {{
            font-size: 3rem;
            margin-left: 15px;
            color: #FFFFFF;
        }}
        .snow-trend-up {{ color: red; }}
        .snow-trend-down {{ color: blue; }}
        .air-trend-up {{ color: red; }}
        .air-trend-down {{ color: blue; }}
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
        a {{
            text-decoration: none;
            color: #FFFFFF;
        }}
    </style>
</head>
<body>
    <div class="header">Välkommen till Lindbäcksstadion!</div>
    <div class="temperature-container">
        <div class="temperature-row">
            <span class="snow snow-temp">Snön {snow_temp}°C</span>
            <span class="trend-arrow {snow_trend_class}">↑</span>
        </div>
        <div class="temperature-row">
            <span class="air air-temp">Luften {air_temp}°C</span>
            <span class="trend-arrow {air_trend_class}">↓</span>
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
