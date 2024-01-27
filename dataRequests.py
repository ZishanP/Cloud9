import requests
from datetime import timedelta, date

def fetch_data_for_date(date):
    url = f'https://cloud9-data-8c815c4bd89c.herokuapp.com/flights?date={date}'
    response = requests.get(url)

    if response.status_code != 200:
        print(f'Error fetching data for {date}')
        return None
    
    return response.json()

# TO RUN:
# data_for_a_day = fetch_data_for_date('2022-11-27')  # replace with an actual date in YYYY-MM-DD format
