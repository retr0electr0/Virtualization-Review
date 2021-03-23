"""
Virtualization Review: Scraper
"""
from bs4 import BeautifulSoup
import requests
import csv

baseurl = 'https://virtualizationreview.com/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
}

# Creating or appending a .csv file
csv_file = open('Virtualization Review.csv', 'a')

# Headers for the .csv file
fieldnames = ['Platform', 'Asset', 'Asset_link', 'Company', 'Type', 'Date Posted']
writer = csv.DictWriter(csv_file, delimiter=',', lineterminator='\n', fieldnames=fieldnames)
writer.writeheader()

productlinks = []

# Getting the list of asset urls
for x in range(1, 2):
    r = requests.get(f'https://virtualizationreview.com/whitepapers/list/vrt-tech-library-list.aspx?Page={x}')
    soup = BeautifulSoup(r.content, 'lxml')
    for i in range(0, 10):
        productlist = soup.find_all('li', id=f'ph_pcontent2_1_lvItemList_liListItem_{i}')
        for item in productlist:
            for link in item.find_all('a', href=True):
                productlinks.append(link['href'])

# Opening the urls from the list one by one and scraping the data out of it
for link in productlinks:
    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')

    name = soup.find('div', id='whitepaper').h4.text.strip()

    company = []

    for c in soup.find_all('img', class_='sponsorlogo'):
        comp_name = c['src'].split('Logos/')[1].split('.ashx')[0].split('/veeampropartner')[0]
        company.append(comp_name)

    date = link.split('/')[5]

    asset = {
        'name': name,
        'company': ' & '.join(company),
        'date': f'{date}.01.2021 MONTH ONLY'
    }
    print(asset)

    # Writing to .csv file
    writer.writerow({'Platform': 'Virtualization Review', 'Asset': name, 'Asset_link': link,
                     'Company': ' & '.join(company), 'Type': 'White Paper', 'Date Posted': f'{date}.01.2021 MONTH ONLY'})

csv_file.close()
