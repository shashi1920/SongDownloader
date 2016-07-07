import requests
response = requests.head('http://hindimasti.net/bollywood/files/New%20Latest%202016/Kapoor%20&%20Sons/Buddhu%20Sa%20Mann.mp3')

print response.headers['content-type']