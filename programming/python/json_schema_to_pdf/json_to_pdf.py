#!/usr/bin/env python

#import json
#import pprint
import time
import types

from reportlab.pdfgen import canvas
from reportlab.lib.colors import black
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Frame, Paragraph, Table, TableStyle


#def get_descriptions(subschema_list):


def create_subschema_table(data, subschema_list):
    """Return a flattened list in the following format:

      [(description, values), (description, values), ...]

    etc.
    """

    tables = []
    value_set = []

    #if subschema_list:
    #    subschema_list_humanized = ' '.join(subschema_list) + ':\n'
    #else:
    #    subschema_list_humanized = ''
    #print('%s%s' %
    #      (subschema_list_humanized, pprint.pformat(data, indent=4)))

    for key in sorted(data.keys()):

        if type(data[key]) in (types.DictType, ):
            base_subschema_list = subschema_list + [key]
            if data[key]:
                object_tables = []
                #object_tables.append((_key, _value))
                tables.extend(object_tables)
                value = 'See "%s" table' % \
                        (' '.join(base_subschema_list))
            else:
                value = '<Empty>'

        elif type(data[key]) in (types.ListType, ):
            base_subschema_list = subschema_list + [key]
            for i, item in enumerate(data[key]):
                _subschema_list = base_subschema_list + ['- index %d' % i]
                item_tables = []
                #subschema_tables = \
                #    create_subschema_table(item, _subschema_list)
                tables.extend(item_tables)
            if data[key]:
                value = 'See "%s" table' % \
                        (' '.join(base_subschema_list))
            else:
                value = '<Empty>'
        else:
            value = data[key]

        value_set.append((key, value))

    subschema_description = ' '.join(subschema_list)
    if subschema_description:
        subschema_description += ' Table'

    return [(subschema_description, value_set)] + tables


def json_to_pdf(data, schema, pdf_filename):
    """Builds a table of 3 values:

    Property | Value | Description
    """

    #table_keys = [('Property', 'Value', 'Description')]
    table_keys = [('Property', 'Value')]

    schema_tables = create_subschema_table(data, subschema_list=[])

    # Inspired by:
    # http://stackoverflow.com/questions/2252726/how-to-create-pdf-files-in-python
    story = []

    styles = getSampleStyleSheet()
    h1 = styles['h1']
    story.append(Paragraph('Summary', h1))
    story.append(Paragraph('Report generated on %s' %
                           (time.strftime('%Y/%m/%d')), styles['Normal']))

    #print('Schema tables:\n%s' % (pprint.pformat(schema_tables), ))

    for schema_description, schema_table in schema_tables:

        story.append(Paragraph(schema_description, h1))

        table_to_print = table_keys + schema_table

        #print('Table to print:\n%s' % (pprint.pformat(table_to_print), ))

        t = Table(table_to_print)
        t.setStyle(TableStyle([
            ('INNERGRID', (0,0), (-1,-1), 0.25, black),
            ('BOX', (0, 0), (-1, -1), 0.25, black),
        ]))
        story.append(t)

    c = canvas.Canvas(pdf_filename)
    f = Frame(inch, inch, 7*inch, 10*inch, showBoundary=1)
    f.addFromList(story, c)
    c.save()


