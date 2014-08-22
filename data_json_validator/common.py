import json
import jsonschema
import re

def validate_data_json(data_json):
    result = []
    try:
        with open('/usr/lib/ckan/tools/data_json_validator/data-json-schema.json') as schema_file:
            schema = json.load(schema_file)
        validator = jsonschema.Draft4Validator(schema)
        for validation_error in validator.iter_errors(data_json):
            result.append(remove_u_prefix(remove_2nd_paragraph(str(validation_error))))
    except Exception as error:
        result.append(error.message)
    return result

def remove_u_prefix(string):
    return re.sub(r"u'([^']*)'", r"'\1'", string)

def remove_2nd_paragraph(string):
    return re.sub(r"\n\n.*\n\n", "\n\n", string)
