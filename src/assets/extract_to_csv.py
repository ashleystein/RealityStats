import requests
from bs4 import BeautifulSoup
from datetime import date
import pandas as pd
from src.utils import clean_strings, remove_leading_chars
from src import aws
from pathlib import Path
from dagster import asset
from src.assets.scrape_wiki import save_wiki_html
@asset(deps=[save_wiki_html])
def extract_to_csv(save_wiki_html):
    vals = []
    html_file = save_wiki_html['html_file']
    show = save_wiki_html['show']
    season = save_wiki_html['season']
    if show == 'traitors':
        csv_file = f"./data/traitors_wiki_raw.csv"
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

                    dic = {'season': season, 'name': name, 'age': age, 'hometown': hometown, 'debut': debut, 'affiliation': affiliation,
                           'finish': finish}
                    vals.append(dic)

    if show == 'bachelorette':
        csv_file = f"./data/bachelorette_wiki_raw.csv"
        with open(html_file, 'r') as f:
            contents = f.read()
            for tr in BeautifulSoup(contents, "html.parser").find_all('tr'):
                td = tr.find_all('td')

                if td and len(td) >= 4:
                    name = clean_strings(td[0])
                    age = clean_strings(td[1], type='age')
                    hometown = clean_strings(td[2])
                    occupation = clean_strings(td[3])
                    try:
                        outcome = clean_strings(td[4])
                    except:
                        outcome = ""
                    try:
                        place = clean_strings(td[5])
                    except:
                        place = ""

                    dic = {'season': season, 'name': name, 'age': age, 'hometown': hometown, 'occupation': occupation, 'outcome': outcome,
                           'place': place}
                    vals.append(dic)
    df = pd.DataFrame(vals)
    df.to_csv(csv_file, mode="a", header=False, index=False)
    return {"csv_file": csv_file, "show": show, "season": season}
