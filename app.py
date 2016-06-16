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

session = {}

@app.route('/timer', methods=['GET', 'POST'])
def create_timer():

	rData = request.get_json(silent=True)

	message = rData['item']['message']['message']

	room_id = rData['item']['room']['id']

	cmd = HTBCommand(message)

	if (cmd.command == 'CONFIG'):
		register_token(room_id, cmd.name)
		notify_room(room_id, 'Token gespeichert :D')

	if (cmd.command == 'NEW'):
		start_timer(room_id, cmd)

	return 'created timer with 10 minutes'

def notify_room(room_id, message):

	if (room_id not in session):
		return

	url = 'https://bindoc.hipchat.com/v2/room/' + room_id + '/notification?auth_token=' + session[room_id]

	headers = {'Content-type': 'application/json'}

	payload = {'color': 'green','message': message,'notify': True,'message_format': 'text'}

	r = requests.post(url, headers = headers, data = json.dumps(payload))

	if r.status_code >= 400:
		log.info('request turns info %d', r.status_code)
		log.info('payload= %s', json.dumps(payload))
		log.info('url= %s', r.url)
		log.info('content= %s', r.content)

def set_scheduler(cmd, room_id, token):

	message_str = '%s mit %d min abgelaufen' % (cmd.name, cmd.minutes)

	Timer(60 * cmd.minutes, notify_room, (room_id, message_str)).start()

def start_timer(room_id, cmd):

	if (room_id not in session): return

	if (cmd.minutes == None): return

	if (cmd.name == None): return

	message_str = '%s mit %d min gestartet ...' % (cmd.name, cmd.minutes)

	notify_room(room_id, message_str)

	set_scheduler(cmd, room_id, session[room_id])


def register_token(room_id, token):
	if (room_id not in session):
		item = {room_id : token}
		session.update(item)

if __name__ == '__main__':

	logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

	# Bind to PORT if defined, otherwise default to 5000.
	port = int(os.environ.get('PORT', 5000))

	app.run(host='0.0.0.0', port=port)