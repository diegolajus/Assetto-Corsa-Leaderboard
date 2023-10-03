import requests
from bs4 import BeautifulSoup

def get_urls():
    # website content
    url = 'https://wastedtime.emperorservers.com/results'
    response = requests.get(url)
    html_content = response.content

    soup = BeautifulSoup(html_content, "html.parser")

    # Find all <tr> elements with class "row-link"
    itemsWithLinks = soup.find_all("tr", class_="row-link")

    # Initialize an empty list to store the data-href values
    data_links = []

    # Iterate through the found elements
    for item in itemsWithLinks:
        # Check if the element has a data-href attribute
        if 'data-href' in item.attrs:
            data_link_value = item['data-href']
            data_links.append(f"https://wastedtime.emperorservers.com{data_link_value}")

    # Print the list of data-href values
    print("List",data_links)
    return data_links