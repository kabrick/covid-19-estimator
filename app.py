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
    g.start = time.time()

@app.after_request
def log_request(response):
    now = time.time()
    duration = round(now - g.start, 2)

    file1 = open("logger.txt", "a")
    file1.write(request.method + "  " + request.path + "  " + str(response.status_code) + "  " + str(duration) +"s \n")
    file1.close()

    return response

@app.route('/api/v1/on-covid-19/logs', methods=['GET'])
def read_logged_data():
    file1 = open("logger.txt", "r")
    return_text = file1.readlines()
    file1.close()
    return Response(return_text, mimetype='text/plain')

@app.route('/api/v1/on-covid-19', methods=['POST'])
def receive_data():
    file1 = open("logger.txt", "a")
    file1.write(str(request.form) +" \n")
    file1.write(str(request.content_type) +" \n")
    file1.close()
    if request.form.get("data") == None:
        return jsonify(estimator.estimator(request.json))
    else:
        return jsonify(estimator.estimator(json.loads(request.form.get("data"))))

@app.route('/api/v1/on-covid-19/json', methods=['POST'])
def receive_data_json():
    return jsonify(estimator.estimator(json.loads(request.form.get("data"))))

@app.route('/api/v1/on-covid-19/xml', methods=['POST'])
def receive_data_xml():
    return Response(dicttoxml(estimator.estimator(json.loads(request.form.get("data")))), mimetype='text/xml')

if __name__ == "__main__":
    app.run()