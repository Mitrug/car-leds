import flask
from car_led import activate_led_profile as car_led

app = flask.Flask(__name__)

@app.route('/led/<int:profile_id>/activate', methods=['PATCH'])
def http_activate_led_profile(profile_id):
    try:
        car_led.activate_led_profile(profile_id)
        
        return flask.Response(status=204)    
    except ValueError:
        return flask.Response(status=404)

    
if __name__ == '__main__':   
	app.run(host='0.0.0.0', port = 8090);
