import os.path

activate_this = os.path.join(os.path.expanduser('~ckan'), 'ckan_default', 'bin', 'activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

import sys
sys.path.append(os.path.join(os.path.expanduser('~ckan'), 'tools'))

from data_json_dashboard import app as application
 