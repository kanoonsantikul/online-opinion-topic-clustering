import json
import os

from flask import Flask
from flask import render_template, json, request

import pandas

app = Flask(__name__)

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))


def load_data(algorithm, file_name):
    result_folder = '../data/results'
    data = pandas.read_csv(os.path.join(SITE_ROOT, result_folder, algorithm, file_name))
    return data.to_json()

@app.route('/', methods=['GET', 'POST'])
def index_render():
    algorithm = request.args.get('algorithm')
    if not algorithm:
        algorithm = 'iterative_new_sdc'
    
    data = request.args.get('data')
    if not data:
        data = 'TescoLotus'
    file_name = data + '.csv'

    json_string_data = load_data(algorithm, file_name)  
    return render_template('index.html', data=json_string_data, algorithm=algorithm, dataName=data)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)