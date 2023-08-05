import os
import sys
import copy
import re
from fnmatch import fnmatch

try:
    import json
except:
    import simplejson as json

#TODO: iterators
class JsonTable(list):
    def __init__(self, jstr):
        if jstr == None:
            list.__init__(self, [])
        elif isinstance(jstr, list):
            list.__init__(self, jstr)
        else:
            open('/tmp/pouet.txt', 'w').write(jstr)
            jstr = re.sub('\s', '', jstr).replace('\\', '')
            open('/tmp/pouet2.txt', 'w').write(jstr)

            jdata = json.loads(jstr)

            if isinstance(jdata, list):
                pass
            elif jdata.has_key('ResultSet'):
                jdata = jdata['ResultSet']['Result']

            list.__init__(self, jdata)

    def dump(self, file_location, leading=[], trailing=[], sep=','):
        fd = open(file_location, 'wb')
        fd.write(self.dumps(leading, trailing, sep))
        fd.close()

    def dumps(self, leading=[], trailing=[], sep=','):
        sep_rpl = '.' if sep != '.' else ','

        if self != []:
            csv = '\n'.join( [ sep.join([ str(val).replace(sep, sep_rpl) 
                                          for val in row
                                        ])
                               for row in self.as_list(leading, trailing)
                             ]
                           )

        return csv

    def as_list(self, leading=[], trailing=[]):
        between = [ header
                    for header in self.get_headers() 
                    if header not in leading and header not in trailing
                  ]

        ordered_headers = leading + between + trailing

        return [ ordered_headers ] + \
               [ [ row[header] 
                   for header in ordered_headers 
                   if self.has_header(header)
                 ]
                 for row in self
               ]

    def has_header(self, name):
        if self != []:
            return name in self.get_headers()
        return False

    def get_headers(self):
        if self != []:
            return self[0].keys()    
        return []

    def get_column(self, col_name, col_filter='*'):
        if col_filter == '*' and '*' not in col_name:
            return self.fget_column(col_name)

        return [ entry[col_name] 
                 for entry in \
                 self.get_subtable([col_name]).kwfilter({col_name:col_filter})
               ]

    def fget_column(self, col_name):
        return [ entry[col_name] 
                 for entry in self.fget_subtable([col_name])
               ]

    def get_subtable(self, col_names=[]):
        if any(['*' in col_name for col_name in col_names]):
            col_names = set(col_name 
                            for col_name in col_names 
                            for key in self.get_headers()
                            if fnmatch(key, col_name))

        return self.fget_subtable(col_names)

    def fget_subtable(self, col_names=[]):
        sub_table = copy.deepcopy(self)

        rmcols = set(self.get_headers()).difference(col_names)

        for entry in sub_table:
            for col in rmcols:
                del entry[col]

        return self.__class__(sub_table)

    def kwfilter(self, kwargs):
        sub_table = \
            [ self[i]
              for i, filter_entry in enumerate(self.get_subtable(kwargs.keys()))
              if all([ fnmatch(str(filter_entry[key]), kwargs[key])
                       for key in filter_entry.keys()
                    ])
            ]
       
        return self.__class__(sub_table)

    def vfilter(self, fvals):
        return self.__class__(
                        json.dumps([ entry
                                     for entry in self
                                     if all([ fval in entry.values()
                                              for fval in fvals
                                           ])
                                  ])
                             )

    def as_dict(self, key_header, vals_h=[]):
        return dict([(entry[key_header], [entry[val_h] for val_h in vals_h]) 
                      for entry in self
                      ])

