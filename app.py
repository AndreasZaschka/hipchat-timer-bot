import os
import requests
import logging
import sys
import json

from flask import Flask

app = Flask(__name__)

log = logging.getLogger('TimerBot')

@app.route('/timer/<int:minutes>/<string:room_id>/<string:token>', methods=['GET', 'POST'])
def create_timer(minutes, room_id, token):

	log.info('create timer with %d minutes for room %s with token %s', minutes, room_id, token)

	url = 'https://bindoc.hipchat.com/v2/room/' + room_id + '/notification?auth_token=' + token

	payload = [ {'color': 'green','message': 'Timer gestartet ...','notify': True,'message_format': 'text'} ]

	r = requests.post(url, json.dumps(payload))

	if r.status_code >= 400:
		log.info('request turns info %d', r.status_code)
		log.info('payload= %s', json.dumps(payload))
		log.info('content= %s', r.content)

	return 'created timer with %d' % minutes

if __name__ == '__main__':

	logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

	# Bind to PORT if defined, otherwise default to 5000.
	port = int(os.environ.get('PORT', 5000))

	app.run(host='0.0.0.0', port=port)