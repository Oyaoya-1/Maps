import requests
from bs4 import BeautifulSoup


url = "https://www.airbnb.co.id/s/Eropa/homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&price_filter_input_type=2&price_filter_num_nights=5&channel=EXPLORE&place_id=ChIJhdqtz4aI7UYRefD8s-aZ73I&date_picker_type=calendar&source=structured_search_input_header&search_type=filter_change"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get(url, headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

images = soup.select('img')
for image in images:
    print(image['src'])