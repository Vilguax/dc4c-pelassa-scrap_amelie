import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "http://annuairesante.ameli.fr/"

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.165 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    'Referer': 'http://annuairesante.ameli.fr/'
}

cookies = {
    'infosoins': 'amobjjidropq8spgj510jscmd2',
    'AmeliDirectPersist': '1651564855.42527.0000',
    'xtvrn': '$475098$',
    'TS01b76c1f': '0139dce0d2edc84ef2fc40c7003637d3083f3ee1f7f7255b071f9ebf8a607495ecb705436d9cd9cdfde9fca735113ea4ac278543f7'
}

data = {
    'ps_profession_label': 'Médecin généraliste',
    'ps_localisation': 'HERAULT (34)'
}

results_per_page = 20
max_results = 1000

medecins_data = []
nom_medecins = set()

page = 1

while len(medecins_data) < max_results:
    page_url = f"http://annuairesante.ameli.fr/professionnels-de-sante/recherche/liste-resultats-page-{page}-par_page-{results_per_page}-tri-aleatoire.html"

    response = requests.get(page_url, headers=headers, cookies=cookies)
    soup = BeautifulSoup(response.text, 'html.parser')

    medecins = soup.find_all('div', class_='item-professionnel-inner')

    if len(medecins) == 0:
        break

    for medecin in medecins:
        nom = medecin.find('h2').get_text() if medecin.find('h2') else None
        tel = medecin.find('div', class_='item left tel').get_text() if medecin.find('div', class_='item left tel') else None
        adresse = medecin.find('div', class_='item left adresse').get_text() if medecin.find('div', class_='item left adresse') else None

        if nom and nom not in nom_medecins:
            medecins_data.append({'Nom': nom, 'Téléphone': tel, 'Adresse': adresse})
            nom_medecins.add(nom)

    page += 1

    if page > 50:
        break

df = pd.DataFrame(medecins_data)
df.to_csv('result.csv', index=False)