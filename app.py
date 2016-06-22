import os
import requests
import logging
import sys
import json
import time

from threading import Timer
from flask import Flask
from flask import request
from command import HTBCommand

app = Flask(__name__)

log = logging.getLogger('TimerBot')

@app.route('/test', methods=['GET', 'POST'])
def create_status():
	return 'ok'


@app.route('/timer', methods=['GET', 'POST'])
def create_timer():

	rData = request.get_json(silent=True)

	message = rData['item']['message']['message']

	room_id = rData['item']['room']['id']

	cmd = HTBCommand(message)

	if (cmd.command == 'NEW'):
		start_timer(room_id, cmd)

	return 'created timer'

def notify_room(room_id, message):

	token = os.environ.get('TOKEN_' + str(room_id), None)

	if (token == None):
		return

	url = 'https://bindoc.hipchat.com/v2/room/' + str(room_id) + '/notification?auth_token=' + token

	headers = {'Content-type': 'application/json'}

	payload = {'color': 'green','message': message,'notify': True,'message_format': 'text'}

	r = requests.post(url, headers = headers, data = json.dumps(payload))

	if r.status_code >= 400:
		log.error('request turns info %d', r.status_code)
		log.error('payload= %s', json.dumps(payload))
		log.error('url= %s', r.url)
		log.error('content= %s', r.content)

def set_scheduler(cmd, room_id):

	message_str = '%s (%d min) abgelaufen' % (cmd.name, cmd.minutes)

	Timer(60 * cmd.minutes, notify_room, (room_id, message_str)).start()

def start_timer(room_id, cmd):

	if (cmd.minutes == None): return

	if (cmd.name == None): return

	message_str = '%s (%d min) gestartet ...' % (cmd.name, cmd.minutes)

	notify_room(room_id, message_str)

	set_scheduler(cmd, room_id)

if __name__ == '__main__':

	logging.basicConfig(stream=sys.stdout, level=logging.ERROR)

	# Bind to PORT if defined, otherwise default to 5000.
	port = int(os.environ.get('PORT', 5000))

	app.run(host='0.0.0.0', port=port)