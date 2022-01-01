import requests
from bs4 import BeautifulSoup
import pandas as pd


def extract(page):
    headers = {"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0"}
    url = f"https://www.olx.ro/locuri-de-munca/munca-in-strainatate/?page={page}"
    r = requests.get(url, headers)
    soup = BeautifulSoup(r.content, 'html.parser')
    return soup


def transform(soup):
    divs = soup.find_all('div', class_='offer-wrapper')
    for item in divs:
        title = item.find('a').text.strip()
        try:
            salariu = item.find('div', class_='list-item__price').text.strip()
        except:
            salariu = ""
        locatia = item.find('p', class_="lheight16").text.strip()
        headers = {"User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:93.0) Gecko/20100101 Firefox/93.0"}
        descrierea = item.find('a').get('href')
        q = requests.get(descrierea, headers)
        ciorba = BeautifulSoup(q.content, 'html.parser')
        descrierea1 = ciorba.find('div', class_='css-2t3g1w-Text').text
        try:
            detalii = ciorba.find('li', class_='css-x9ckc').text
        except:
            detalii = ''

        job = {
            'titlu': title,
            'Salariu': salariu,
            'Locatia': locatia,
            'Descriere': descrierea1,
            'Detalii': detalii,
            'Link catre anunt': descrierea
        }
        joblist.append(job)
    return


joblist = []
for i in range(0, 20, 5):
    print(f'Pagina la care este, {i}')
    c = extract(0)
    transform(c)

df = pd.DataFrame(joblist)
print(df.head())
df.to_csv('jobs4.csv')
