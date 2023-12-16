import requests
import time

def check_online(player_id):
    timestamp = time.time()
    data = {'player_id': player_id, 'timestamp': timestamp}
    response = requests.post('http://192.168.10.9:5000/check_online', json=data)
    
    if response.status_code == 200:
        print('Successfully checked online status.')
    else:
        print('Error checking online status.')

def get_online_players():
    response = requests.get('http://192.168.10.9:5000/get_online_players')
    
    if response.status_code == 200:
        online_players = response.json()
        print('Online Players:', online_players)
    else:
        print('Error getting online players.')

if __name__ == '__main__':
    player_id = input('Enter your player ID: ')
    
    check_online(player_id)
    get_online_players()
