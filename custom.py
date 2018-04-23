#!flask/bin/python3
from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import url_for
from flask import Response

from datetime import timedelta
from pytz import timezone
import time
import datetime
import pytz

import socket
import pickle
from zeroconf import __version__, ServiceInfo, Zeroconf

#setup the zeroconf stuff here
r = Zeroconf()

desc = {'version': '0.10', 'a': 'test value', 'b': 'another value'}
info = ServiceInfo("_http._tcp.local.",
                   "My Service Name2._http._tcp.local.",
                   socket.inet_aton("0.0.0.0"), 5000, 0, 0, desc)

r.register_service(info)

app = Flask(__name__)

times = [
    {
        'id': 0,
        'City': u'New York City, NY',
        'TimeZone': u'US/Eastern', 
    },
    {
        'id': 1,
        'City': u'Austin, TX',
        'TimeZone': u'US/Central', 
    }
]
@app.route('/custom/times', methods=['GET', 'POST'])
def get_post_times():
    if(request.method == 'GET'):
        return jsonify({'times': times})
    elif(request.method == 'POST'):
        data = request.form
        t = {
            'id': times[-1]['id'] + 1,
            'City': data['City'], #request.json['City', ""],
            'TimeZone': data['TimeZone'] #request.json('TimeZone', ""),
        }
        times.append(time)
        return return jsonify(t), 201
    
@app.route('/custom/times/<int:time_id>', methods=['GET'])
def get_time(time_id):
    time = [time for time in times if time['id'] == time_id]
    if len(time) == 0:
        abort(404)
    for x in times:
        if x['id'] == time_id:
            cityTimeZoneString = str(x['TimeZone'])
            cityNameString = str(x['City'])   
            tz = pytz.timezone(cityTimeZoneString) 
            cityNow = datetime.datetime.now(tz)
            timeString = cityNow.strftime("%H:%M:%S %m-%d-%Y") 
            cityDataString = "The current time in " + cityNameString + " is " + timeString +"\n"
            return cityDataString

@app.route("/custom/times/currentTime", methods=['GET'])
def currentTime():
   now = datetime.datetime.now().time()
   timeString = "The current time is " + now.strftime("%H:%M:%S %m-%d-%Y") + " UTC\n"  #Create a formatted string using the date and time from the now object
   return timeString

@app.route('/custom/times/<int:time_id>', methods=['POST'])
def create_time(time_id):
    data = request.form
    t = {
        'id': time_id,
        'City': data['City'],
        'TimeZone': data['TimeZone']
    }
    times.append(t)
    return jsonify(t), 201
    #return Response(response='Success: \n', status=201)
    
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == "__main__": #If this script was run directly from the command line
   app.run(host='0.0.0.0', port=5000, debug=True)
