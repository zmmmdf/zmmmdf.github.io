import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin
from tqdm import tqdm
import time

data = []

total_pages = 35

for i in tqdm(range(total_pages), desc="Downloading Pages"):
    url = f"https://www.eolymp.com/en/users/mziya/submissions?page={i}"

    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')

    tbody_elements = soup.find_all('tbody')

    for tbody in tbody_elements:
        tr_elements = tbody.find_all('tr')

        for tr in tr_elements:
            solution_href = urljoin(url, tr.find('a', class_='eo-solution-status')['href'])
            problem_href = urljoin(url, tr.find_all('a')[1]['href'])
            problem_title = tr.find_all('a')[1].text
            cells = tr.find_all('td', class_='mdl-data-table__cell--non-numeric')
            id = lang_text = cells[0].text.strip()
            lang = lang_text = cells[3].text.strip()
            if 'Accepted' in tr.text:
                data.append({
                    'solution_href': solution_href,
                    'problem_href': problem_href,
                    'problem_title': problem_title,
                    'lang': lang,
                    'id': id
                })

with open('./data/eolymp.json', 'w') as f:
    json.dump(data, f, indent=4)
print("Data has been successfully scraped and saved to submisssions.json")
print("Total number of submissions:", len(data))
