# scraper.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import config

class LeaderboardScraper:
    def __init__(self, url):
        self.url = url

    def get_html_content(self):
        response = requests.get(self.url)
        return response.content

    def extract_data_from_card(self, card):
        card_laptime = card.find("div", class_="float-right")
        card_header = card.find("div", class_="card-header")
        ranking_position = card_header.text.strip().split('\n')[0].split()[0]
        pilot_name = card_header.text.strip().split('\n')[0].split()[1]
        car_name = card_header.text.strip().split('\n')[7].strip()
        lap_time = card_laptime.text.strip().split('\n')[1].strip().replace('Potential:', '').strip(",")
        lap_time = "Invalid lap" if lap_time == "00:00.000" else lap_time

        return ranking_position, pilot_name, car_name, lap_time
    
    def generate_table_row(self, ranking_position, pilot_name, car_name, lap_time, i):
        if lap_time == "Invalid lap":
            return f"<tr><td>{ranking_position}</td><td id=f{pilot_name}>{pilot_name}</td><td>{car_name}</td><td id='invalid-lap'>{lap_time}</td></tr>"
        if i == 1:
            return f"<tr id='gold'><td>{ranking_position}</td><td id=f{pilot_name}>{pilot_name}</td><td>{car_name}</td><td>{lap_time}</td></tr>"
        elif i == 2:
            return f"<tr id='silver'><td>{ranking_position}</td><td id=f{pilot_name}>{pilot_name}</td><td>{car_name}</td><td>{lap_time}</td></tr>"
        elif i == 3:
            return f"<tr id='bronze'><td>{ranking_position}</td><td id=f{pilot_name}>{pilot_name}</td><td>{car_name}</td><td>{lap_time}</td></tr>"
        else:
            return f"<tr><td>{ranking_position}</td><td>{pilot_name}</td><td>{car_name}</td><td>{lap_time}</td></tr>"


    def get_used_cars(self, cards):
        used_cars = set()
        for card in cards[1:]:
            _, _, car_name, lap_time = self.extract_data_from_card(card)
            if lap_time != "Invalid lap":
                used_cars.add(car_name)
        return list(used_cars)

    def generate_filter_options(self, used_cars):
        options = ""
        for car in used_cars:
            options += f"<option value='{car}'>{car}</option>"
        return options

    def scrape_leaderboard(self):
        html_content = self.get_html_content()
        soup = BeautifulSoup(html_content, "html.parser")
        current_date = datetime.now().strftime("%dth %b")
        cards = soup.find_all("div", class_="card")
        used_cars = self.get_used_cars(cards)

        with open(config.FILE_NAME, "w", encoding="utf-8") as file:
            # Starting HTML FILE
            file.write(f"""
            <html>
                <head>
                    <link rel='stylesheet' href='styles.css'>
                </head>
                <body>
                    <p class='title'>Nordschleife Leaderboard</p> 
                    <p class='update'>Last Update: {current_date} </p>
                <div class='header-container'>
                    <div>
                        <input type="text" id="searchInput" onkeyup="searchTable()" placeholder="Search for names..">
                    </div>
                    <div>
                        <select id="carFilter" onchange="filterByCar()">
                            <option value="">All Cars</option>
                            {self.generate_filter_options(used_cars)}
                        </select>
                    </div>
                    <div>
                        <p class='server-link'><a href='https://acstuff.ru/s/q:race/online/join?httpPort=9649&ip=148.251.236.163' target='_blank'> Play </a></p>
                    </div>
                    <div>
                        <a href='https://discord.gg/4SGcjFGS' target='_blank'>
                            <img src='https://cdn-icons-png.flaticon.com/512/2111/2111370.png' alt='Join our Discord server'>
                        </a>
                    </div>
                </div>                      
                    <table id="leaderboardTable">
                        <tr><th>Ranking Position</th><th>Pilot Name</th><th>Car Name</th><th>Lap Time</th></tr>
            """)

            for i, card in enumerate(cards):
                if i != 0:
                    ranking_position, pilot_name, car_name, lap_time = self.extract_data_from_card(card)
                    table_row = self.generate_table_row(ranking_position, pilot_name, car_name, lap_time, i)
                    file.write(table_row)

            # Ending of HTML file
            file.write("</table>")
            file.write("<script>")
            file.write("function searchTable() {")
            file.write("var input, filter, table, tr, td, i, txtValue;")
            file.write("input = document.getElementById('searchInput');")
            file.write("filter = input.value.toUpperCase();")
            file.write("table = document.getElementById('leaderboardTable');")
            file.write("tr = table.getElementsByTagName('tr');")
            file.write("for (i = 0; i < tr.length; i++) {")
            file.write("td = tr[i].getElementsByTagName('td')[1];")
            file.write("if (td) {")
            file.write("txtValue = td.textContent || td.innerText;")
            file.write("if (txtValue.toUpperCase().indexOf(filter) > -1) {")
            file.write("tr[i].style.display = '';}")
            file.write("else {tr[i].style.display = 'none';}")
            file.write("}}}")

            file.write("function filterByCar() {")
            file.write("var input, filter, table, tr, td, i, txtValue;")
            file.write("input = document.getElementById('carFilter');")
            file.write("filter = input.value.toUpperCase();")
            file.write("table = document.getElementById('leaderboardTable');")
            file.write("tr = table.getElementsByTagName('tr');")
            file.write("for (i = 1; i < tr.length; i++) {")
            file.write("td = tr[i].getElementsByTagName('td')[2];")
            file.write("if (td) {")
            file.write("txtValue = td.textContent || td.innerText;")
            file.write("if (filter === '' || txtValue.toUpperCase() === filter) {")
            file.write("tr[i].style.display = '';}")
            file.write("else {tr[i].style.display = 'none';}")
            file.write("}}}")
            file.write("</script>")
            file.write("</body></html>")

        print("---- ITEMS WERE ADDED ----")