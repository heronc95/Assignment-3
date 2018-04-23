import requests
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--IP_ADDRESS", help="This is the ip address of the custom.py flask server that is running", type=str)
parser.add_argument("-p", "--PORT", help="Specific Port Number of custom.py server. In our case it is 5000", type=str)

# This gets the arguments from the user
args = parser.parse_args()
addr = args.IP_ADDRESS
port = args.PORT

URL = "http://" + str(addr) +":" + str(port) + "/"

#Get Requests
responseGet1 = requests.get(URL+'custom/times', auth=('admin', 'pass'))
responseGet2 = requests.get(URL+'custom/times/0', auth=('admin', 'pass'))
responseGet3 = requests.get(URL+'custom/times/currentTime', auth=('admin', 'pass'))


#Put Requests Data
cityData1 = [
    ('City', 'Denver, CO'),
    ('TimeZone', 'US/Mountain'),
]

cityData2 = [
    ('City', 'Los Angeles, CA'),
    ('TimeZone', 'US/Pacific'),
]

#Put Request
responsePut1 = requests.post(URL+'custom/times', data=cityData1, auth=('admin', 'pass'))
responsePut2 = requests.post(URL+'custom/times/5', data=cityData2, auth=('admin', 'pass')) 


#PRINT GET RESPONSE HEADERS AND BODY
print(str(responseGet1.headers) + "\n")
print(str(responseGet1.text) + "\n")
print(str(responseGet2.headers) + "\n")
print(str(responseGet2.text) + "\n")
print(str(responseGet3.headers) + "\n")
print(str(responseGet3.text) + "\n")


#PRINT POST RESPONSE HEADERS AND BODY
print('\n' + str(responsePut1.headers) + '\n')
print(str(responsePut1.text) + '\n')
print(str(responsePut2.headers) + '\n')
print(str(responsePut2.text))
