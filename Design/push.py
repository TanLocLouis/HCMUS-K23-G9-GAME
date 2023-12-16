import requests
try:
	url = 'http://192.168.10.9:2000'
	files = {'file': open('players.xlsx', 'rb')}
	response = requests.post(url, files=files, timeout=0.1)
except:
	print("Server is not reachable.")