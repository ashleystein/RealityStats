import requests
from bs4 import BeautifulSoup
from datetime import date
import pandas as pd
from utils import clean_strings
from src import aws

# from html_form_to_dict import html_form_to_dict as html2dict
dt = date.today().strftime("%Y-%m-%d")

def scrapePage(url):
    secret_name = 'agent_for_wiki_scraping'
    agent = aws.get_secret(secret_name)

    try:
        response = requests.get(
            url=url, headers={'user-agent': agent['UserAgent']}
        )
        return BeautifulSoup(response.content, 'html.parser')
    except Exception:
        print('Error occurred while getting the page, ' + Exception)


def get_html(url, file_name):
    file = f"{file_name}_{dt}"
    soup = scrapePage(url)
    text = soup.find_all('table', class_="wikitable sortable")
    with open(file, "w") as f:
        f.write(str(text))


def saveToCsv(df, csv_name):
    file = csv_name + '.csv'
    df.to_csv(file, index=False)


def get_next_page_imdb(curr, soup):
    """
    Returns the link to the next page
    from imdb page
    :param curr: current page
    :param soup:
    :return:
    """
    link = soup.find_all('a', class_='flat-button lister-page-next next-page')
    if len(link) == 1:
        return link[0].attrs['href']
    else:
        return False


def extract_to_csv(html_file, csv_file):
    vals = []
    with open(html_file, 'r') as f:
        contents = f.read()
        for tr in BeautifulSoup(contents, "html.parser").find_all('tr'):
            td = tr.find_all('td')
            th = tr.find_all('th')
            if th[0].find('span') is not None:
                name = th[0].find('span').text

            if td and len(td) >= 4:
                age = clean_strings(td[0])
                hometown = clean_strings(td[1])
                debut = clean_strings(td[2])
                affiliation = clean_strings(td[3])
                try:
                    finish = clean_strings(td[4])
                except:
                    finish = ""

                dic = {'name': name, 'age': age, 'hometown': hometown, 'debut': debut, 'affiliation': affiliation,
                       'finish': finish}
                # print(f"name:{name}")
                vals.append(dic)
    df = pd.DataFrame(vals)
    df.to_csv(csv_file, index=False)


get_html('https://en.wikipedia.org/wiki/The_Bachelorette_(American_TV_series)_season_21', 'bachelorette_s21')
#extract_to_csv('html_files/bachelorette_s21', 'traitors_us_s4_2026-02-25.csv')
#get_secret('agent_for_wiki_scraping')
