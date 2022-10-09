from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin
import unicodedata 
import pandas as pd

def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s)
                if unicodedata.category(c) != 'Mn')


root_url = requests.get("https://www.zlatestranky.sk/").text.encode('utf-8').decode('ascii', 'ignore')
root_content = BeautifulSoup(root_url, "html.parser")
hladanie1_url = requests.get("https://www.zlatestranky.sk/hladanie/restauracie+a+bary/1/").text.encode('utf-8').decode('ascii', 'ignore')
hladanie1_content = BeautifulSoup(hladanie1_url, "html.parser")
hladanie2_url = requests.get("https://www.zlatestranky.sk/hladanie/restauracie+a+bary/2/").text.encode('utf-8').decode('ascii', 'ignore')
hladanie2_content = BeautifulSoup(hladanie2_url, "html.parser")

titles = []
page = 1
for i in range(1,10):
    url = f"https://www.zlatestranky.sk/hladanie/restauracie+a+bary/{page}/"
    response = requests.get(url).text.encode('utf-8').decode('ascii', 'ignore')
    soup = BeautifulSoup(response, "html.parser")
    titles.append(soup)
    page = page + 1
#print(titles)


def get_urls(link):
    a = []
    key_words = ["Restaurant", "restaurant", "bar", "Bar", "Re%C5%A1taur%C3%A1cia", "re%C5%A1taur%C3%A1cia" ]
    for li in link.find_all("a", class_ = "t-fpbc"):
        ab = li.get("href")
        if any(word in ab for word in key_words):
                if ab not in a:
                    a.append(ab)
    return a



def find_icons():
    url = "https://www.zlatestranky.sk/"
    url_join = []
    for title in titles:
        for l in get_urls(title):
            if l != None:
                url_join.append(urljoin(url, l))
        firma = []
        adresa = []
        telefon = []
        email = []
     
        for url in url_join:
            root = requests.get(url).text
            soup = BeautifulSoup(root, 'html.parser')
            adress_ul = soup.find("ul", class_ = "icons")


            if soup.find("div", class_="col9").find_all("span", class_="tag-phone-main"):
                for cislo in soup.find("div", class_="col9").find_all("span", class_="tag-phone-main"):
                    for c in cislo:
                        telefon.append(c.text)
            else:
                telefon.append("Nothing")

            if soup.find("div", class_="col9").find_all("span", class_= "tag-emails"):
                for mail in soup.find("div", class_="col9").find_all("span", class_= "tag-emails"):
                    for m in mail:
                        email.append(m.text)
            else:
                email.append("Nothing")
        
            if adress_ul.find("span"):
                for adress in adress_ul.find("span"):
                    adresa.append(strip_accents(adress.text.lower()))

            else:
                adresa.append("Nothing")

            if soup.find("h1", class_="bold tag-name"):
                for firm in soup.find("h1", class_="bold tag-name"):
                    firma.append(strip_accents(firm.text.lower()))
            else:
                firma.append("Nothing")

    col1 = "firma"
    col2 = "adresa"
    col3 = "telefon"
    col4 = "email"
    data = pd.DataFrame({col1:firma,col2:adresa,col3:telefon,col4:email})
    data.to_excel('Zlate_stranky_scrapped.xlsx', sheet_name='Zlate_stranky_scrapped', index=False)

    
    return firma, adresa, telefon, email



find_icons()