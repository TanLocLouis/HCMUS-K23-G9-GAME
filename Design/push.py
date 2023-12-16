import requests
try:
	url = 'http://game.tltech.asia/'
	files = {'file': open('players.xlsx', 'rb')}
	response = requests.post(url, files=files, timeout=3)
except:
	print("Server is not reachable.")