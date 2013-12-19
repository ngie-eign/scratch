#!/usr/bin/env python

import pprint
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

    def subschema_list_to_description(subschema_list):
        subschema_description = ' '.join(subschema_list)
        if subschema_description:
            subschema_description += ' Table'
        return subschema_description


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
            if data[key]:
                base_subschema_list = subschema_list + [key]
                object_tables = create_subschema_table(data[key],
                                                       base_subschema_list)
                tables.extend(object_tables)
                value = 'See "%s" table' % \
                        (' '.join(base_subschema_list))
            else:
                value = '<Empty>'

        elif type(data[key]) in (types.ListType, ):
            if data[key]:
                base_subschema_list = subschema_list + [key]
                item_tables = []
                for i, item in enumerate(data[key]):
                    _subschema_list = base_subschema_list + ['- index %d' % i]
                    if type(item) in (types.DictType, ):
                        item_tables.extend((key, create_subschema_table(item,
                                            _subschema_list)))
                    else:
                        item_tables.append(('', item))
                tables.append(
                    (subschema_list_to_description(base_subschema_list),
                     item_tables))
                value = 'See "%s" table' % \
                        (' '.join(base_subschema_list))
            else:
                value = '<Empty>'
        else:
            value = data[key]

        value_set.append((key, value))

    subschema_description = subschema_list_to_description(subschema_list)

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

    c = canvas.Canvas(pdf_filename)
    f = Frame(inch, inch, 7*inch, 10*inch, showBoundary=1)

    story = [
        Paragraph('Summary', h1),
        Paragraph('Report generated on %s' %
                  (time.strftime('%Y/%m/%d')), styles['Normal']),
    ]
    f.addFromList(story, c)
    c.showPage()

    #print('Schema tables:\n%s' % (pprint.pformat(schema_tables), ))

    for schema_description, schema_table in schema_tables:

        f = Frame(inch, inch, 7*inch, 10*inch, showBoundary=1)
        story = [
            Paragraph(schema_description, h1),
        ]
        table_contents  = table_keys
        for prop, value in schema_table:
            table_contents.append((prop,
                                   Paragraph(str(value), styles['Normal'])))

        t = Table(table_contents, colWidths=(2.5 * inch, 4 * inch))
        t.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BOX', (0, 0), (-1, -1), 0.25, black),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(t)
        f.addFromList(story, c)
        c.showPage()

    c.save()


if __name__ == '__main__':
    import json
    import os
    import sys

    if len(sys.argv) != 4:
        sys.exit('usage: %s file.json schema.json output.pdf'
                 % (os.path.basename(sys.argv[0]), ))

    with open(sys.argv[1]) as json_fd:
        #with open(sys.argv[2]) as json_schema_fd:
        json_to_pdf(json.load(json_fd), {}, sys.argv[3])
