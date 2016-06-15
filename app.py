import os
import requests
import logging
import sys

from flask import Flask

app = Flask(__name__)

log = logging.getLogger('HipchatTimerBot')

@app.route('/timer/<int:minutes>/<string:room_id>/<string:token>', methods=['GET', 'POST'])
def create_timer(minutes, room_id, token):

	log.info('create timer with %d minutes for room %s with token %s', minutes, room_id, token)

	url = 'https://bindoc.hipchat.com/v2/room/' + room_id + '/notification?auth_token=' + token

	log.info('url = %s', url)

	r = requests.post(url, data = {'color': 'green','message': 'Timer gestartet ...','notify': true,'message_format': 'text'})

	log.info('request turns info')

	return 'created timer'

if __name__ == '__main__':

	logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

	# Bind to PORT if defined, otherwise default to 5000.
	port = int(os.environ.get('PORT', 5000))

	log.info('set port successfully')

	app.run(host='0.0.0.0', port=port)