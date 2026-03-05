import pandas as pd
from src import utils
from dagster import asset


@asset
def get_not_scraped_url():
    df = pd.read_csv('./data/wiki_urls.csv', dtype=str)
    scraping = df[df['scraped'] != 'TRUE'][:1][['show', 'season', 'url']]
    row = scraping.values[0]
    show = utils.remove_leading_chars(row[0], 'the')
    return {"show": show, "season": row[1], "url": row[2]}


@asset
def update_analytics_page_data(extract_to_csv):
    """Depends on extract_to_csv; receives its return dict (csv_file path, show, season)."""
    csv_file = f"./data/{extract_to_csv['csv_file']}"
    show = extract_to_csv["show"]
    season = extract_to_csv["season"]
    df = pd.read_csv(csv_file)
    new_df = pd.DataFrame(columns=["Contestant", "Show", "Season", "Instagram Id", "IG Follower Count"])
    new_df["Contestant"] = df["name"]
    new_df["Show"] = show
    new_df["Season"] = season

    with open("analytics_page.csv", "a") as f:
        new_df.to_csv(f, header=False)