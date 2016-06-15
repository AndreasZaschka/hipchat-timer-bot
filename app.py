import os
import requests
import logging
import sys
import json
import time

from threading import Timer
from flask import Flask
from flask import request

app = Flask(__name__)

log = logging.getLogger('TimerBot')

token = None

@app.route('/timer', methods=['GET', 'POST'])
def create_timer():

	if request.headers.get('Content-Type') == 'application/json':
		rData = request.get_json(silent=True)
		rJson = json.load(rData)
		message = rJson['item']['message']['message']
		room_id = rJson['item']['room']['id']

		log.info('message = %s', message)
		log.info('room_id = %s', room_id)

	#log.info('create timer with %d minutes for room %s with token %s', minutes, room_id, token)

	#notify_room(room_id, token, 'Timer gestartet ...')

	#set_scheduler(minutes, room_id, token)

	return 'created timer with 10 minutes'

def notify_room(room_id, token, message):

	url = 'https://bindoc.hipchat.com/v2/room/' + room_id + '/notification?auth_token=' + token

	headers = {'Content-type': 'application/json'}

	payload = {'color': 'green','message': message,'notify': True,'message_format': 'text'}

	r = requests.post(url, headers = headers, data = json.dumps(payload))

	if r.status_code >= 400:
		log.info('request turns info %d', r.status_code)
		log.info('payload= %s', json.dumps(payload))
		log.info('url= %s', r.url)
		log.info('content= %s', r.content)

def set_scheduler(minutes, room_id, token):

	Timer(60 * minutes, notify_room, (room_id, token, 'Timer abgelaufen')).start()

if __name__ == '__main__':

	logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

	# Bind to PORT if defined, otherwise default to 5000.
	port = int(os.environ.get('PORT', 5000))

	app.run(host='0.0.0.0', port=port)