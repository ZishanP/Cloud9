import requests
from bs4 import BeautifulSoup

# Replace 'your-url-here' with the actual URL you want to scrape
url = 'https://cloud9-data-8c815c4bd89c.herokuapp.com/flights?date=2022-12-26'

try:
    # Send an HTTP GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Print the parsed HTML content (you can modify this as needed)
        print(soup.prettify())
    else:
        print(f'Failed to retrieve data. Status Code: {response.status_code}')

except requests.exceptions.RequestException as e:
    print(f'An error occurred: {e}')
