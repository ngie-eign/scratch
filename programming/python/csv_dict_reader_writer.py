#!/usr/bin/env python
"""A csv.{DictReader,Writer} test app
"""

from collections import OrderedDict
import cStringIO
import csv
import sys
import traceback

nfields = 10

d = OrderedDict([('f_' + str(i), str(i)) for i in xrange(nfields)])

fieldnames = d.keys()
spurious_fieldnames = fieldnames + ['extra']
less_fieldnames = fieldnames[:-3]

use_exec = True


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
        sys.stdout.write('dr_kwargs: %s\n' % (dr_kwargs, ))
        reader = csv.DictReader(f, **dr_kwargs)
        for j, line in enumerate(reader, start=1):
            sys.stdout.write('Line %03d: %s (type=%s)\n'
                             % (j, line, type(line), ))

            # The former idiom will work in all cases, but it causes pylint to
            # complain about undefined variables referenced later on in the
            # code.
            #
            # The latter idiom doesn't suffer from this caveat, but results in
            # a tuple unpack error if the field names don't match the fields
            # in a row.
            #
            # This is a programming error :)..
            if use_exec:
                for field in fieldnames:
                    exec('%s = line.get(field)' % (field, ))
            else:
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

            sys.stdout.write('Values %03d: %s\n'
                             % (j, ', '.join(map(str,
                                                 (f_0, f_1, f_2, f_3, f_4,
                                                  f_5, f_6, f_7, f_8, f_9,
                                                  )))))

    finally:
        f.close()


sys.stdout.write('Exact number of fields\n')
print_csv(fieldnames)

sys.stdout.write('Spurious fields\n')
print_csv(spurious_fieldnames)

sys.stdout.write('Less fields without leftovers\n')
try:
    print_csv(less_fieldnames)
except ValueError:
    sys.stdout.write('OK (raised a ValueError). The exception '
                     'received was:\n%s\n'
                     % (traceback.format_exc(), ))

sys.stdout.write('Less fields with leftovers\n')
print_csv(less_fieldnames, with_leftovers=True)
