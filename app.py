import os
import requests

from flask import Flask

app = Flask(__name__)

@app.route('/timer/<int:minutes>/<string:room_id>/<string:token>', methods=['GET', 'POST'])
def createTimer(minutes, room_id, token):

	url = 'https://bindoc.hipchat.com/v2/room/' + room_id + '/notification?auth_token=' + token

	r = requests.post(url, data = {
  				'color': 'green', 
  				'message': 'Timer gestartet ...', 
  				'notify': true, 
  				'message_format': 'text'
				})

    return 'created timer'

if __name__ == '__main__':

    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)