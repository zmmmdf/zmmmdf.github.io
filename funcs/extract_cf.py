import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin
from tqdm import tqdm
import time

data = []

total_pages = 1

for i in tqdm(range(total_pages), desc="Downloading Pages"):
    url = f"https://codeforces.com/submissions/ziyam/page/{i}"

    # Send a GET request to the URL
    response = requests.get(url)
    time.sleep(0.5)  # Add a small delay to avoid overloading the server

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    # Write the data to a JSON file
    with open('index.html', 'w') as f:
        f.write(soup.find("html"))

    tbody_elements = soup.find_all('tbody')


    # Loop through each tbody element
    for tbody in tbody_elements:

        tr_elements = tbody.find_all('tr', class_="highlighted-row")

        for tr in tr_elements:
            cells = tr.find_all('td')

            id = lang_text = cells[0].find('a').text.strip()
            solution_href = urljoin(url, cells[0].find('a')['href'])
            problem_href = urljoin(url, cells[3].find('a')['href'])

            problem_title = cells[3].find('a')['href'].text.strip()

            lang = lang_text = cells[4].text.strip()
            # Check if the solution is accepted
            if 'Accepted' in cells[5].text:
                # Add the data to the list
                data.append({
                    'solution_href': solution_href,
                    'problem_href': problem_href,
                    'problem_title': problem_title,
                    'lang': lang,
                    'id': id
                })

# Write the data to a JSON file
with open('./data/codeforces.json', 'w') as f:
    json.dump(data, f, indent=4)
print("Data has been successfully scraped and saved to codeforces.json")
print("Total number of submissions:", len(data))
