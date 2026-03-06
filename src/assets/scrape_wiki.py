import requests
from bs4 import BeautifulSoup
from datetime import date
from src import aws
from dagster import asset
from src import utils
from datetime import datetime, timedelta
from pathlib import Path
from src.assets.refresh_analytics import get_not_scraped_url
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

@asset
def save_wiki_html(get_not_scraped_url):
    show = get_not_scraped_url['show']
    season = get_not_scraped_url['season']
    url = get_not_scraped_url['url']

    file_name = f"./html_files/{show}_{season}"
    # Only scrape if it hasn't been scraped and
    # the last scrape was at least 3 days ago.
    if utils.does_file_exist(file_name):

        last_modified_time = utils.get_last_modified_time(file_name)

        if datetime.now() - last_modified_time < timedelta(days=3):
            print(f"{file_name} already exist, returning location.")
            return {"html_file": file_name, "show": show, "season": season}
    else:
        soup = scrapePage(url)

        text = soup.find_all('table', class_="wikitable sortable")
        with open(file_name, "w") as f:
            f.write(str(text))
        print(f"Saved to {file_name}")
        return {"html_file": file_name, "show": show, "season": season}

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

