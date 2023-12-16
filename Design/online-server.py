from flask import Flask, request, jsonify
import time

app = Flask(__name__)
online_players = {}

def remove_inactive_players():
    current_time = time.time()
    inactive_players = [player_id for player_id, last_activity_time in online_players.items() if current_time - last_activity_time >= 10]
    
    for player_id in inactive_players:
        del online_players[player_id]

@app.route('/check_online', methods=['POST'])
def check_online():
    data = request.get_json()
    player_id = data.get('player_id')
    timestamp = data.get('timestamp')

    current_time = time.time()
    if current_time - timestamp < 10:
        online_players[player_id] = current_time

    remove_inactive_players()

    return jsonify({'status': 'success'})

@app.route('/get_online_players', methods=['GET'])
def get_online_players():
    remove_inactive_players()
    return jsonify(online_players)

if __name__ == '__main__':
    app.run(debug=True)
# if you want to run on Docker
    app.run(host='0.0.0.0', port=5000, debug=True)
