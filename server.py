from pymongo import MongoClient
from functools import wraps
from flask import Flask, request, Response
from zeroconf import Zeroconf
import socket
import pickle
import requests
from canvas_token import authentication

import requests



collection = None
client = None

r = Zeroconf()



# Setup for the canvas API stuff here
auth = authentication()
canvas_key = auth.getcanvas_key()
canvas_url = auth.getcanvas_url()
download_filename = 'hello.txt'
upload_filename   = 'hello.txt'
# Set up a session
session = requests.Session()
session.headers = {'Authorization': 'Bearer %s' % canvas_key}











# # Step 3 - download file
# r = requests.get(canvas_url+'/'+download_filename, allow_redirects=True)
# #open(download_filename, 'wb').write(r.content)
# r = r.json()  # The requests now works and returns response 200 - not 301.
# print(' ')
# print(r)  # This is a dictionary containing some info about the downloaded file




def get_file_from_canvas(download_filename):
    return requests.get(canvas_url + '/' + download_filename, allow_redirects=True)
    # open(download_filename, 'wb').write(r.content)
    # r = r.json()  # The requests now works and returns response 200 - not 301.
    # print(' ')
    # print(r)  # This is a dictionary containing some info about the downloaded file


def push_file_to_canvas(upload_filename, file):
    # Step 1 - tell Canvas you want to upload a file
    payload = {}
    payload['name'] = upload_filename
    payload['parent_folder_path'] = '/'
    r = session.post(canvas_url, data=payload)
    r.raise_for_status()
    r = r.json()
    # Step 2 - upload file
    payload = list(r['upload_params'].items())  # Note this is now a list of tuples

    #with open(upload_filename, 'rb') as f:
    #    file_content = f.read()
    file_content = file.read()

    payload.append((u'file', file_content))  # Append file at the end of list of tuples
    r = requests.post(r['upload_url'], files=payload)
    r.raise_for_status()
    return r

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

data = {'red': 0.0, 'blue': 0.0, 'green': 0.0, 'rate': 0.0, 'state': 1}

@app.route('/led', methods=['GET', 'POST'])
@requires_auth
def index():
    if request.method == 'GET':
        info = None
        info = r.get_service_info("_http._tcp.local.", "My Service Name._http._tcp.local.")
        if info:
            return Response(status=200, response=str(data))
        else:
            return Response(response="LED resource is not ready",
                            status=503)
    elif request.method == "POST":
        data_sent = request.form # a dict
        if 'red' in data_sent:
            data['red'] = data_sent['red']
        if 'green' in data_sent:
            data['green'] = data_sent['green']
        if 'blue' in data_sent:
            data['blue'] = data_sent['blue']
        if 'rate' in data_sent:
            data['rate'] = data_sent['rate']
        if 'state' in data_sent:
            data['state'] = data_sent['state']
 
        # do the sending to the led here
        info = r.get_service_info("_http._tcp.local.", "My Service Name._http._tcp.local.")
        if info:
            TCP_IP = str(socket.inet_ntoa(info.address)) #'0.0.0.0'
            TCP_PORT = int(info.port)
            MESSAGE = data

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((TCP_IP, TCP_PORT))
            s.send(pickle.dumps(MESSAGE))
            s.close()
            return Response(response="Success", status=200) 
        else:
            return Response(response="LED resource is not ready",
                            status=503)


# @app.route('/canvas', methods=['GET', 'POST'])
# @requires_auth
# def canvas():
#     if request.method == 'GET':
#         info = r.get_service_info("_http._tcp.local.", "My Service Name._http._tcp.local.")
#         if info:
#             return Response(status=200, response=str(data))
#         else:
#             return Response()

@app.route('/canvas/download', methods=['GET'])
@requires_auth
def canvas_download():
    print("here")

    if request.method == 'GET':
        print(request)
        filename = request.args.get('filename')
        print(filename)
        get_file_from_canvas(filename)
        return Response(response="Success", status=200)
    else:
        return Response(status=400, response='Failed')


@app.route('/canvas/upload', methods=['POST'])
@requires_auth
def canvas_upload():
    if request.method == 'POST':
        r = request
        # check if the post request has the file part
        #if 'file' not in request.files:
        filename = r.args['filename']
        file = r.files[filename]

        push_file_to_canvas(filename, file)
        return Response(response="Success", status=200)

    else:
        return Response(status=400)




if __name__ == '__main__':

    # before running the server, setup the values
    # open the pymongo client to use
    client = MongoClient('mongodb://localhost:27017/')

    # Get the database to use
    db = client.http_auth_database
    collection = db.auth_collection

    # run the server now
    app.run(host='0.0.0.0', port=5000, debug=True)




