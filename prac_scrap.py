import requests
from bs4 import BeautifulSoup


url = "https://clist.by/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get(url, headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

contest = soup.find_all('div', {
    'class': ['contest', 'row']
}) 

for contest in contest:
    start_time = contest.select_one('.start-time')
    if not start_time:
        continue
    start_time = start_time.text.strip()
    duration = contest.select_one('.duration').text.strip()
    timeleft = contest.select_one('.timeleft').text.strip()
    event_name = contest.select_one('.title_search').text.strip()
    print(start_time, duration, timeleft, event_name)