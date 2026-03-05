from dagster import Definitions, load_assets_from_modules

from src.assets import extract_to_csv, refresh_analytics, scrape_wiki

# Load all assets from the imported modules
all_assets = load_assets_from_modules([extract_to_csv, refresh_analytics, scrape_wiki])

defs = Definitions(
    assets=all_assets,

)