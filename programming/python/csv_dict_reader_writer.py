#!/usr/bin/env python

from collections import OrderedDict
import cStringIO
import csv
import traceback

nfields = 10

d = OrderedDict([('f_' + str(i), str(i)) for i in xrange(nfields)])

fieldnames = d.keys()
spurious_fieldnames = fieldnames + ['extra']
less_fieldnames = fieldnames[:-3]

def print_csv(field_names, with_leftovers=False):

    f = cStringIO.StringIO()
    try:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(d)
        f.seek(0)

        dr_kwargs = {'fieldnames': field_names}
        if with_leftovers:
            restkey = 'EXTRAS'

            dr_kwargs.update({
                'restkey': restkey,
            })
        print('dr_kwargs: %s' % dr_kwargs)
        reader = csv.DictReader(f, **dr_kwargs)
        for i, line in enumerate(reader, start=1):
            print('Line %03d: %s (type=%s)' % (i, line, type(line), ))

            for field in fieldnames:
                exec('%s = line.get(field)' % (field, ))

            if False:
                (
                f_0,
                f_1,
                f_2,
                f_3,
                f_4,
                f_5,
                f_6,
                f_7,
                f_8,
                f_9,
                ) = tuple([line.get(field) for field in field_names])
            print('Values %03d: %s' % (i,
                                       ', '.join(map(str,
                                                     (f_0, f_1, f_2, f_3, f_4,
                                                      f_5, f_6, f_7, f_8, f_9, )))))

    finally:
        f.close()

print('Exact number of fields')
print_csv(fieldnames)

print('Spurious fields')
print_csv(spurious_fieldnames)

print('Less fields without leftovers')
try:
    print_csv(less_fieldnames)
except ValueError:
    print('OK (raised a ValueError). The exception received was:\n%s'
          % (traceback.format_exc(), ))

print('Less fields with leftovers')
print_csv(less_fieldnames, with_leftovers=True)
