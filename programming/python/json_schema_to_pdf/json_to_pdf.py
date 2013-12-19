#!/usr/bin/env python

import pprint
import time
import types

from reportlab.pdfgen import canvas
from reportlab.lib.colors import black
from reportlab.lib.styles import (
                                  getSampleStyleSheet,
                                  ParagraphStyle,
                                  )
from reportlab.lib.units import inch
from reportlab.platypus import (
                                BaseDocTemplate,
                                Frame,
                                PageTemplate,
                                Paragraph,
                                Table,
                                TableStyle,
                                )


#def get_descriptions(subschema_list):


def create_subschema_table(data, subschema_list):
    """Return a flattened list in the following format:

      [(description, values), (description, values), ...]

    etc.
    """

    def subschema_list_to_description(subschema_list):
        return '%s Table' % (' '.join(subschema_list) or 'Root')


    tables = []
    value_set = []

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


class PdfTemplate(BaseDocTemplate):


    def __init__(self, *args, **kwargs):
        BaseDocTemplate.__init__(self, *args, **kwargs)


    def afterPage(self):

        self.canv.saveState()
        self.canv._x = 0
        self.canv._y = 0
        self.canv.restoreState()


def json_to_pdf(data, schema, pdf_filename):
    """Builds a table of 3 values:

    Property | Value | Description
    """

    styles = getSampleStyleSheet()

    #table_keys = ['Property', 'Value', 'Description']
    table_keys = ['Property', 'Value']

    table_keys = [[Paragraph(key, styles['h3']) for key in table_keys]]

    schema_tables = create_subschema_table(data, subschema_list=[])
    styles = getSampleStyleSheet()

    # Inspired by:
    # http://stackoverflow.com/questions/2252726/how-to-create-pdf-files-in-python
    elements = [
        Paragraph('Report generated on %s' % (time.strftime('%Y/%m/%d')),
                  styles['h2'])
    ]

    h1 = styles['h1']

    doc = PdfTemplate(
        pdf_filename,
        rightMargin = 0.3 * inch,
        leftMargin = 0.3 * inch,
        topMargin = 0.3 * inch,
        bottomMargin = 0.3 * inch,
    )

    for schema_description, schema_table in schema_tables:

        # XXX: the ` ` paragraphs are hacks around the fact that I don't know
        # how to flow text properly to pad the tables.
        elements.extend([
            Paragraph(' ', h1),
            Paragraph(schema_description, h1),
            Paragraph(' ', h1),
        ])
        table_contents = list(table_keys)
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
        elements.append(t)
    doc.addPageTemplates(PageTemplate('normal',
                         [Frame(inch, inch, 7*inch, 10*inch, showBoundary=1)]))
    doc.build(elements)


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
