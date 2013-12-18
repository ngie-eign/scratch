import jsonschema

import json_to_pdf

DATA = {
    'a': 'b',
    'c': {
        'd': 'e',
    },
    'f': [
        'g',
        'h'
    ],
    'i': [
    ],
    'j': {
    }
}

SCHEMA = {
    'type': 'object',
    'properties': {
        'a': {
            'description': 'First letter',
        },
        'c': {
            'type': 'object',
            'description': 'Third letter',
            'properties': {
                'd': {
                    'type': 'string',
                    'description': 'Fourth letter',
                },
            },
        },
        'f': {
            'type': 'array',
            'description': 'Sixth letter',
            'minItems': 1,
        },
        'i': {
            'type': 'array',
            'description': 'Ninth letter',
        },
        'j': {
            'type': 'object',
            'description': 'Tenth letter',
        },
    }
}

jsonschema.validate(DATA, SCHEMA)

json_to_pdf.json_to_pdf(DATA, SCHEMA, 'out.pdf')
