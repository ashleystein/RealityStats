import requests
from bs4 import BeautifulSoup
from datetime import date
import pandas as pd
from utils import clean_strings, remove_leading_chars
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


def save_wiki_html(url, file_name):
    file = f"./html_files/{file_name}_{dt}"
    #  check if it already exists

    soup = scrapePage(url)
    text = soup.find_all('table', class_="wikitable sortable")
    with open(file, "w") as f:
        f.write(str(text))
    print(f'saved to {file}')

    return file


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

def get_not_scraped_url():
    df = pd.read_csv('./data/wiki_urls.csv', dtype=str)
    scraping = df[df['scraped'] != 'TRUE'][:1][['show', 'season', 'url']]
    return scraping.values[0][0], scraping.values[0][1], scraping.values[0][2]


show, season, scraping_url = get_not_scraped_url()
show_name = remove_leading_chars(show, 'the')
file_name = f"{show_name}_{str(season)}"
html_file = save_wiki_html(scraping_url, file_name)
extract_to_csv(html_file=html_file, csv_file=file_name)
