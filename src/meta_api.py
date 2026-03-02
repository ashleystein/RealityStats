import requests
import csv
import pandas as pd
from src import aws


def get_clean_string(x):
  return x.text.replace('\n', '')

def capture_instagram_numbers(json_data_list, filename):

    for json_data in json_data_list:

        profile_info = json_data['business_discovery']

        # Writing to CSV
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            # Use the keys from the dictionary as headers
            writer = csv.DictWriter(file, fieldnames=profile_info.keys())

            # Write the header row
            writer.writeheader()

            # Write the data row
            writer.writerow(profile_info)

    print(f"Data successfully saved to {filename}")


def get_instagram_business_info(access_token, my_ig_id, target_username):
    """
    Fetches public info from a target Instagram account using Business Discovery.
    """
    # The endpoint URL (using the latest stable Graph API version)
    url = f"https://graph.facebook.com/v22.0/{my_ig_id}"

    # Define the fields we want to discover about the target user
    # Note: we are looking up 'target_username' through 'my_ig_id'
    fields = f"business_discovery.username({target_username}){{name,username,followers_count,media_count}}"

    params = {
        'fields': fields,
        'access_token': access_token
    }

    try:
        #print(params)
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises an error for 4XX or 5XX responses
        return response.json()
    except requests.exceptions.HTTPError as err:
        return f"HTTP error occurred: {err}\nResponse: {response.text}"
    except Exception as err:
        return f"An error occurred: {err}"


#
# --- CONFIGURATION ---
secret_json = aws.get_secret('fb_long_term_access_token')
ACCESS_TOKEN = secret_json['access_token']
MY_IG_ID = secret_json['my_ig_business_account_id'] # Your Instagram Business Account ID
insta_numbers_file = '../insta_numbers.csv'

df = pd.read_csv('../data/instagram_profile_data.csv')
username = df['insta_username']
data_list = []
# Execute
# for un in username:
#     data = get_instagram_business_info(ACCESS_TOKEN, MY_IG_ID, un)
#     print(data)
#     data_list.append(data)
#capture_instagram_numbers(data_list, insta_numbers_file)

