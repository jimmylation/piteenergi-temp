def update_log_file(timestamp, snow_temp, air_temp, updated_time):
    try:
        with open(log_file, "r") as file:
            soup = BeautifulSoup(file, "html.parser")
            table = soup.find("table")
    except FileNotFoundError:
        # Om loggfilen inte finns, skapa en ny tabell
        soup = BeautifulSoup("", "html.parser")
        table = None

    # Om tabellen inte hittas, skapa en ny tabell
    if table is None:
        table = soup.new_tag("table", style="width: 90%; margin: 30px auto; border-collapse: collapse; background-color: #fafafa;")
        header_row = soup.new_tag("tr")
        headers = ["Tid", "Uppdaterad Tid", "Snötemp (°C)", "Lufttemp (°C)"]
        for header in headers:
            th = soup.new_tag("th", style="padding: 12px; background-color: #4CAF50; color: white; font-size: 1.2em; text-align: center;")
            th.string = header
            header_row.append(th)
        table.append(header_row)

    # Lägg till en ny rad med data (nyaste data hamnar först)
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

    # Lägg till den nya raden högst upp i tabellen (nyaste data överst)
    table.insert(1, new_row)  # Index 1 för att lägga till direkt efter headern

    # Begränsa till senaste 3 timmars data (om mer än 91 rader, ta bort den äldsta)
    rows = table.find_all("tr")
    if len(rows) > 91:  # 91 rader = 1 rad för headers + 90 loggade timmar
        rows[-1].extract()  # Ta bort den sista raden (äldsta datan)

    # Spara tabellen i loggfilen
    soup.clear()
    soup.append(table)
    with open(log_file, "w") as file:
        file.write(str(soup))
