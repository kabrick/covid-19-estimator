from flask import Flask, request, jsonify, Response, g
from src import estimator
import json
from dicttoxml import dicttoxml
import datetime
import time

app = Flask(__name__)
app.config["DEBUG"] = True

@app.before_request
def start_timer():
    g.start = time.time() * 1000

@app.after_request
def log_request(response):
    f = open('logger.txt', 'a+')
    req_method = request.method
    req_path = request.path
    res_time = round(time.time() * 1000 - g.start)
    res_status_code = response.status_code

    f.write("{} \t\t {} \t\t {} \t\t {} ms \n".format(req_method, req_path, res_status_code, res_time))
    f.close()

    return response

@app.route('/api/v1/on-covid-19/logs', methods=['GET'])
def read_logged_data():
    f = open('logger.txt', 'r')
    contents = f.read()
    f.close()
    return contents

@app.route('/api/v1/on-covid-19', methods=['POST'])
def receive_data():
    if request.form.get("data") == None:
        return jsonify(estimator.estimator(request.json))
    else:
        return jsonify(estimator.estimator(json.loads(request.form.get("data"))))

@app.route('/api/v1/on-covid-19/json', methods=['POST'])
def receive_data_json():
    if request.form.get("data") == None:
        return jsonify(estimator.estimator(request.json))
    else:
        return jsonify(estimator.estimator(json.loads(request.form.get("data"))))

@app.route('/api/v1/on-covid-19/xml', methods=['POST'])
def receive_data_xml():
    if request.form.get("data") == None:
        return Response(dicttoxml(estimator.estimator(request.json), custom_root="result"), mimetype='application/xml')
    else:
        return Response(dicttoxml(estimator.estimator(json.loads(request.form.get("data"))), custom_root="result"), mimetype='application/xml')

if __name__ == "__main__":
    app.run()