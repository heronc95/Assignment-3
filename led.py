from flask import Flask, request, Response, jsonify


data = {'red': 0.0, 'blue': 0.0, 'green': 0.0, 'rate': 0.0, 'state': 0}

app = Flask(__name__)

@app.route('/led', methods=['GET', 'POST'])
def led():
    if request.method == 'GET':
        # Ask the LED client what it's current state is
        return jsonify(data)
    elif request.method == "POST":
        data_sent = request.form # a dict
        passed = False
        if 'red' in data_sent:
            data['red'] = data_sent['red']
            passed = True
        if 'green' in data_sent:
            data['green'] = data_sent['green']
            passed = True
        if 'blue' in data_sent:
            data['blue'] = data_sent['blue']
            passed = True
        if 'rate' in data_sent:
            data['rate'] = data_sent['rate']
            passed = True
        if 'state' in data_sent:
            data['state'] = data_sent['state']
            passed = True

        if passed:
            return Response("Success", status=200)
        else:
            return Response("Error", status=400)
        # now apply the data to the PWM on the RPI
if __name__ == "__main__":
    app.run(host='localhost', port=9999, debug=True)