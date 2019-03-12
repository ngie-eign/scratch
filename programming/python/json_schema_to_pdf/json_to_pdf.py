#!/usr/bin/env python

import json
import time
import types

from reportlab.lib.colors import black
from reportlab.lib.pagesizes import (
                                     landscape,
                                     letter,
                                     )
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
                                BaseDocTemplate,
                                Frame,
                                PageTemplate,
                                Paragraph,
                                Table,
                                TableStyle,
                                )


def property_description(schema, path=None, path_travelled=None):

    if path_travelled is None:
        path_travelled = []

    if not path or schema.get('type', 'string') not in ('array', 'object', ):
        prop_desc = schema.get('description', '')
        return prop_desc

    path_travelled.append(path.pop(0))
    schema = schema.get('properties', {}).get(path_travelled[-1], {})

    if 'items' in schema:
        schema = schema['items']

    return property_description(schema, path=path,
                                path_travelled=path_travelled)


def create_schema_tables(instance, schema, path):
    """Return a flattened list in the following format:

      [(table_description, values), ...]

      Each of the values inside should be in the following format:

      [(instance_name, value, instance_description]]

    etc.
    """

    def path_to_str(path):
        return ' '.join([str(e) for e in path])


    def _table_description(path):
        return '%s Table' % (path_to_str(path) or 'Root')


    tables = []
    value_set = []

    table_description = _table_description(path)

    for key in sorted(instance.keys()):

        prop_desc = property_description(schema, path=(path + [key]))

        if type(instance[key]) in (types.DictType, ):
            if instance[key]:
                base_path = path + [key]
                object_tables = create_schema_tables(instance[key], schema,
                                                     base_path)
                tables.extend(object_tables)
                value = 'See "%s" table' % (' '.join(base_path))
            else:
                value = '<Empty>'

        elif type(instance[key]) in (types.ListType, ):
            if instance[key]:
                for i, item in enumerate(instance[key]):
                    base_path = path + [key, i]
                    if type(item) in (types.DictType, ):
                        subschema_tables = create_schema_tables(item, schema,
                                                                base_path)
                        tables.extend(subschema_tables)
                    else:
                        if type(item) not in (types.ListType, ):
                            item = [item]
                        tables.append((_table_description(base_path),
                                       [(str(j), table_value, '') \
                                           for j, table_value in
                                                           enumerate(item)]))

                    value = 'See "%s" table(s)' % \
                            (path_to_str(base_path[:-1]), )
            else:
                value = '<Empty>'
        else:
            value = instance[key]

        value_set.append((key, value, prop_desc))

    return [(table_description, value_set)] + tables


class PdfTemplate(BaseDocTemplate):
    """Template for the PDF document"""


    def __init__(self, *args, **kwargs):
        BaseDocTemplate.__init__(self, *args, **kwargs)


    def afterPage(self):
        """afterPage override"""

        self.canv.saveState()
        self.canv._x = 0
        self.canv._y = 0
        self.canv.restoreState()


STYLES = getSampleStyleSheet()
H1_STYLE = STYLES['h1']
H2_STYLE = STYLES['h2']
H3_STYLE = STYLES['h3']
H4_STYLE = STYLES['h4']
NORMAL_STYLE = STYLES['Normal']


def json_to_pdf(instance, schema, pdf_filename):
    """Builds a PDF with tables from a json instance

    TODO: add description support
    """

    table_keys = [
        'Property',
        'Value',
        'Description',
    ]

    table_keys = [[Paragraph(key, H3_STYLE) for key in table_keys]]

    schema_tables = create_schema_tables(instance, schema, [])

    # Inspired by:
    # http://stackoverflow.com/questions/2252726/how-to-create-pdf-files-in-python
    elements = [
        Paragraph('Report generated on %s' % (time.strftime('%Y/%m/%d')),
                  H2_STYLE)
    ]

    doc = PdfTemplate(
        pdf_filename,
        rightMargin = 0.3 * inch,
        leftMargin = 0.3 * inch,
        topMargin = 0.3 * inch,
        bottomMargin = 0.3 * inch,
    )

    #print(json.dumps(schema_tables, indent=4))
    for schema_description, schema_table in schema_tables:

        #print(schema_description)

        # XXX: the ` ` paragraphs are hacks around the fact that I don't know
        # how to flow text properly to pad the tables.
        elements.extend([
            Paragraph(' ', H1_STYLE),
            Paragraph(schema_description, H1_STYLE),
            Paragraph(' ', H1_STYLE),
        ])
        table_contents = list(table_keys)
        #print(json.dumps(schema_table, indent=4))
        for prop, value, description in schema_table:
            table_contents.append(tuple([Paragraph(str(cell_txt), NORMAL_STYLE)
                                             for cell_txt in (prop, value,
                                                              description)]))

        t = Table(table_contents, colWidths=(3 * inch, 3 * inch, 3 * inch))
        t.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('BOX', (0, 0), (-1, -1), 0.25, black),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, black),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        elements.append(t)

    doc.addPageTemplates(PageTemplate('normal',
                         [Frame(inch, inch, 9 * inch, 7 * inch,
                                showBoundary=1)],
                         pagesize=landscape(letter)))
    doc.build(elements)


def main():
    """main"""

    import os
    import sys

    if len(sys.argv) != 4:
        sys.exit('usage: %s file.json schema.json output.pdf'
                 % (os.path.basename(sys.argv[0]), ))

    with open(sys.argv[1]) as json_fd:
        json_text = json_fd.read()

    with open(sys.argv[2]) as json_schema_fd:
        json_schema_text = json_schema_fd.read()

    output_pdf = sys.argv[3]

    json_to_pdf(json.loads(json_text), json.loads(json_schema_text),
                output_pdf)


if __name__ == '__main__':
    main()
