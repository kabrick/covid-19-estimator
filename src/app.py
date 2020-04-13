from flask import Flask, request, jsonify
import estimator
import json

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['POST'])
def receive_data():
    return jsonify(estimator.estimator(json.loads(request.form.get("data"))))

app.run()