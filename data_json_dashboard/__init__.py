import codecs
import ConfigParser
import json
import os.path
from flask import Flask
from flask import render_template

app = Flask(__name__)

def config_section_map(config, section):
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                print('skip: %s' % option)
        except:
            print('exception on %s!' % option)
            dict1[option] = None
    return dict1

@app.route('/')
def dashboard():
    config_file = os.path.join(os.path.expanduser('~ckan'), 'shared', 'config', 'config.ini')
    config = ConfigParser.ConfigParser()
    config.read(config_file)
    provider_urls = config_section_map(config, 'ProviderUrl')
    provider_names = config_section_map(config, 'ProviderName')
    providers = []
    for provider_id, provider_name in provider_names.items():
        check_status_file = os.path.join(os.path.expanduser('~ckan'),
                                         'shared', 'data-json-status', 'check', provider_id)
        harvest_status_file = os.path.join(os.path.expanduser('~ckan'),
                                           'shared', 'data-json-status', 'harvest', provider_id)
        with codecs.open(check_status_file, 'r', 'utf-8') as f:
            try:
                check_status = json.load(f)
            except ValueError:
                check_status = {'timestamp': '', 'result': [], 'resource_count': '', 'dataset_count': ''}
        with codecs.open(harvest_status_file, 'r', 'utf-8') as f:
            try:
                harvest_status = json.load(f)
            except ValueError:
                harvest_status = {'timestamp': '', 'result': []}
        providers.append({'name': provider_name,
                          'url': provider_urls[provider_id],
                          'last_check_time': check_status['timestamp'],
                          'last_harvest_time': harvest_status['timestamp'],
                          'check_result': check_status['result'],
                          'harvest_result': harvest_status['result'],
                          'dataset_count': check_status['dataset_count'],
                          'resource_count': check_status['resource_count']})
    return render_template('page.html', providers=providers)

if __name__ == '__main__':
    app.run()
