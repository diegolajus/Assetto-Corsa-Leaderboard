import requests
from bs4 import BeautifulSoup
import url
import subprocess
from datetime import datetime

# Your Python script code goes here

# After your script finishes running, execute the Bash script
subprocess.run(["bash", "automate_git.sh"])

url_extraction = url.get_urls()

# Obtén el contenido de la página web
url = url_extraction[0]
response = requests.get(url)
html_content = response.content

soup = BeautifulSoup(html_content, "html.parser")

# Format date as "dayth Month" (e.g., 3th Oct)
current_date = datetime.now().strftime("%dth %b")



 # Scrap all <div class="card">
cards = soup.find_all("div", class_="card")

with open("index.html", "w", encoding="utf-8") as file:
    # Starting HTML FILE
    file.write(f"""
    <html>
        <head>
            <link rel='stylesheet' href='styles.css'>
            <style>
                tr:nth-child(1) {{ background-color: gold; }}
                tr:nth-child(2) {{ background-color: silver; }}
                tr:nth-child(3) {{ background-color: #cd7f32; /* Bronze color */ }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
            </style>
        </head>
        <body>
            <p class='title'>Nordschleife Leaderboard</p>
            <input type="text" id="searchInput" onkeyup="searchTable()" placeholder="Search for names..">
            <p class='update'>Last Update: {current_date} </p>
            <p class='server-link'><a href='https://acstuff.ru/s/q:race/online/join?httpPort=9649&ip=148.251.236.163'> Play Here</a></p>
            <table id="leaderboardTable">
                <tr><th>Ranking Position</th><th>Pilot Name</th><th>Car Name</th><th>Lap Time</th></tr>
    """)
    # iteratation over all cards scrapped and select specific targets
    for i, card in enumerate(cards):
        if i != 0:  # Skip the first card (Which is table information row)
            card_laptime = card.find("div", class_="float-right")
            card_header = card.find("div", class_="card-header")
            ranking_position = card_header.text.strip().split('\n')[0].split()[0]
            pilot_name = card_header.text.strip().split('\n')[0].split()[1]
            car_name = card_header.text.strip().split('\n')[7].strip()
            lap_time = card_laptime.text.strip().split('\n')[1].strip().replace('Potential:', '').strip(",")
            lap_time = "Invalid lap" if lap_time == "00:00.000" else lap_time

            # Write a new row in the table
            if i == 1:
                file.write(f"<tr id='gold'><td>{ranking_position}</td><td>{pilot_name}</td><td>{car_name}</td><td>{lap_time}</td></tr>")
            elif i == 2:
                file.write(f"<tr id='silver'><td>{ranking_position}</td><td>{pilot_name}</td><td>{car_name}</td><td>{lap_time}</td></tr>")
            elif i == 3:
                file.write(f"<tr id='bronze'><td>{ranking_position}</td><td>{pilot_name}</td><td>{car_name}</td><td>{lap_time}</td></tr>")
            else:
                file.write(f"<tr><td>{ranking_position}</td><td>{pilot_name}</td><td>{car_name}</td><td>{lap_time}</td></tr>")

    # Ending of HTML file
    file.write("</table>")
    file.write("<script>")
    file.write("function searchTable() {")
    file.write("var input, filter, table, tr, td, i, txtValue;")
    file.write("input = document.getElementById('searchInput');")
    file.write("filter = input.value.toUpperCase();")
    file.write("table = document.getElementById('leaderboardTable');")
    file.write("tr = table.getElementsByTagName('tr');")
    file.write("for (i = 0; i < tr.length; i++) {")  # Start from index 0 to include the header row
    file.write("td = tr[i].getElementsByTagName('td')[1];")  # Index 1 corresponds to the Pilot Name column
    file.write("if (td) {")
    file.write("txtValue = td.textContent || td.innerText;")
    file.write("if (txtValue.toUpperCase().indexOf(filter) > -1) {")
    file.write("tr[i].style.display = '';}")
    file.write("else {tr[i].style.display = 'none';}")
    file.write("}}}")
    file.write("</script>")
    file.write("</body></html>")

print("---- ITEMS WERE ADDED ----")