from pymongo import MongoClient
from functools import wraps
from flask import Flask, request, Response
import requests
from zeroconf import ServiceBrowser, Zeroconf


collection = None
client = None

def check_auth(username, password):
    """This function is called to check if a username /
    password combination is valid. and inside the mongodb database
    """
    result = collection.find_one({'username': username, 'password': password})
    if result:
        return True
    else:
        return False

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
    'Could not verify your access level for that URL.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


app = Flask(__name__)


@app.route('/led', methods=['GET', 'POST'])
@requires_auth
def index():
    if request.method == 'GET':
        r = requests.get('http://localhost:9999/led')
        # Ask the LED client what it's current state is
        return str(r.content) + str(r.status_code)
    elif request.method == "POST":
        data = request.form
        # do the post here
        post_r = requests.post('http://localhost:9999/led', data)
        #if post_r.status_code == 200:
        return str(post_r.content) + str(post_r.status_code)

if __name__ == '__main__':

    # before running the server, setup the values
    # open the pymongo client to use
    client = MongoClient('mongodb://localhost:27017/')

    # Get the database to use
    db = client.http_auth_database
    collection = db.auth_collection

    # run the server now
    app.run(host='localhost', port=5000, debug=True)


