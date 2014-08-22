import json
from flask import Flask
from flask import render_template
from flask import request
from werkzeug.utils import secure_filename
from data_json_validator import common

app = Flask(__name__)

@app.route('/', methods=['GET'])
def front():
    return render_template('page.html')

@app.route('/', methods=['POST'])
def check():
    result = []
    filename = ''
    try:
        data_file = request.files['data_file']
        filename = secure_filename(data_file.filename)
        data_string = data_file.read().decode('utf-8-sig')
        data_json = json.loads(data_string)
        result = common.validate_data_json(data_json)
    except Exception as error:
        result.append(error.message)
    if not result:
        dataset_count = len(data_json)
        resource_count = 0
        for dataset in data_json:
            resource_count = resource_count + len(dataset['resources'])
    else:
        dataset_count = resource_count = 0
    return render_template('page.html',
                           data=data_string,
                           result=result,
                           dataset_count=dataset_count,
                           resource_count=resource_count,
                           filename=filename)

if __name__ == '__main__':
    app.run()
