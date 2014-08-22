activate_this = '/usr/lib/ckan/ckan_default/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys
sys.path.insert(0, '/usr/lib/ckan/tools')

from data_json_validator import app as application
 