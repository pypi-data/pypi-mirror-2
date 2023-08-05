import os
import hashlib
import tempfile
import glob
import httplib2
import time
from fnmatch import fnmatch

from lxml import etree

import restapi
from jsontable import JsonTable


search_nsmap = { 'xdat':'http://nrg.wustl.edu/security',
                 'xsi':'http://www.w3.org/2001/XMLSchema-instance' }

def build_search_document(root_element_name, columns, criteria_set):
    root_node = \
        etree.Element( etree.QName(search_nsmap['xdat'], 'bundle'),
                       nsmap=search_nsmap
                     )

    root_node.set('ID', "@%s"%root_element_name)
    root_node.set('allow-diff-columns', "0")
    root_node.set('secure', "false")

    root_element_name_node = \
        etree.Element( etree.QName(search_nsmap['xdat'], 'root_element_name'),
                       nsmap=search_nsmap
                     )

    root_element_name_node.text = root_element_name

    root_node.append(root_element_name_node)

    for i, column in enumerate(columns):
        element_name, field_ID = column.split('/')

        search_field_node = \
            etree.Element( etree.QName(search_nsmap['xdat'], 'search_field'), 
                           nsmap=search_nsmap
                         )

        element_name_node = \
            etree.Element( etree.QName(search_nsmap['xdat'], 'element_name'), 
                           nsmap=search_nsmap
                         )

        element_name_node.text = element_name

        field_ID_node = \
            etree.Element( etree.QName(search_nsmap['xdat'], 'field_ID'), 
                           nsmap=search_nsmap
                         )

        field_ID_node.text = field_ID

        sequence_node = \
            etree.Element( etree.QName(search_nsmap['xdat'], 'sequence'), 
                           nsmap=search_nsmap
                         )

        sequence_node.text = str(i)

        type_node = \
            etree.Element( etree.QName(search_nsmap['xdat'], 'type'), 
                           nsmap=search_nsmap
                         )

        type_node.text = 'string'

        header_node = \
            etree.Element( etree.QName(search_nsmap['xdat'], 'header'), 
                           nsmap=search_nsmap
                         )

        header_node.text = column

        search_field_node.extend([ element_name_node,
                                   field_ID_node,
                                   sequence_node,
                                   type_node, header_node
                                ])

        root_node.append(search_field_node)

    search_where_node = \
        etree.Element( etree.QName(search_nsmap['xdat'], 'search_where'), 
                       nsmap=search_nsmap
                     )

    root_node.append(build_criteria_set(search_where_node, criteria_set))

    return etree.tostring(root_node.getroottree())

def build_criteria_set(container_node, criteria_set):

    for criteria in criteria_set:
        if isinstance(criteria, (str, unicode)):
            container_node.set('method', criteria)

        if isinstance(criteria, (list)):
            sub_container_node = \
                etree.Element( etree.QName(search_nsmap['xdat'], 'child_set'),
                               nsmap=search_nsmap
                             )

            container_node.append(
                build_criteria_set(sub_container_node, criteria))

        if isinstance(criteria, (tuple)):
            constraint_node = \
                etree.Element( etree.QName(search_nsmap['xdat'], 'criteria'), 
                               nsmap=search_nsmap
                             )

            constraint_node.set('override_value_formatting', '0')

            schema_field_node = \
                etree.Element( etree.QName( search_nsmap['xdat'],
                                             'schema_field'
                                          ), 
                               nsmap=search_nsmap
                             )

            schema_field_node.text = criteria[0]

            comparison_type_node = \
                etree.Element( etree.QName( search_nsmap['xdat'],
                                            'comparison_type'
                                          ), 
                               nsmap=search_nsmap
                             )

            comparison_type_node.text = criteria[1]

            value_node = \
                etree.Element( etree.QName(search_nsmap['xdat'], 'value'),
                               nsmap=search_nsmap
                             )

            value_node.text = criteria[2]

            constraint_node.extend([
                        schema_field_node, comparison_type_node, value_node])

            container_node.append(constraint_node)

    return container_node

# --------------------------------------------------------------------------- #

class SearchManager(object):
    """ Define constraints to make a complex search on the database.

        A search manager is available as an Interface attribute.
        Its main usage is simply to be called to create a ``Search`` object 
        which will be responsible for specifying the returned data and for
        submitting the actual query.

        Some additional methods are provided to list, retrieve and delete
        saved search.

        Example:
            >>> query = [ ('xnat:subjectData/SUBJECT_ID', 'LIKE', '%'), 
                          ('xnat:projectData/ID', '=', 'my_project'),
                          [ ('xnat:subjectData/AGE', '>', '14'),
                            'AND'
                          ],
                          'OR'
                        ]
            >>> search = interface.search('my_search', query)
            >>>
            >>> # no search is saved because it was not submitted
            >>> interface.search.names()
            []
            >>> # submit and get results
            >>> search.get_subjects()
            [...]
            >>> # now the search is saved
            >>> interface.search.names()
            ['my_search']
            >>> 
            >>> same_search = interface.search.get('my_search')
    """
    def __init__(self, interface):
        self._interface = interface
        self._cachedir = interface._engine._h.cache.cache
        self._cache = interface._engine._h.cache

    def __call__(self, name, query):
        """ Setups and returns a ``Search`` object. 

            .. warning::
                The search itself is not submitted here. The search is executed
                when a Search method like get_subjects(), which defines what
                kind of data is to be returned is called.
                
            Parameters
            ----------
            name: string
                Gives a name to the search to be able to retrieve it later.
                A name must be unique for a specific query.
            query: list
                This is the query that will be submitted to the server
                    A query is an unordered list that contains
                        - 1 or more constraints
                        - 0 or more sub-queries (lists as this one)
                        - 1 comparison method between the constraints 
                            ('AND' or 'OR')
                    A constraint is an ordered tuple that contains
                        - 1 valid searchable_type/searchable_field
                        - 1 operator among '=', '<', '>', '<=', '>=', 'LIKE'

            See also
            --------
            Search.get_table(), Search.get_subjects(), Search.get_experiments()
        """
        return Search(name, query, self._interface)

    def types(self, name_filter='*'):
        """ List the searchable types on the XNAT server.
        """
        elements = JsonTable(self._interface._engine.get_json(
                             '/REST/search/elements')
                             ).fget_column('ELEMENT_NAME')

        return [element_name
                for element_name in elements
                if fnmatch(element_name, name_filter)]

    def type_fields(self, searchable_type, prepend_type=False):
        """ List the searchable fields for the given type on the XNAT server.
        """
        fields = JsonTable(self._interface._engine.get_json(
                           '/REST/search/elements/%s' % searchable_type)
                           ).fget_column('FIELD_ID')

        return ['%s/%s'%(searchable_type, field) if prepend_type else field
                for field in fields 
                if '=' not in field and 'SHARINGSHAREPROJECT' not in field]

    def field_values(self, field_name):
        """ List all the values given to this field on the XNAT server.
        """

        safename = field_name.replace('/', '_').replace(':', '_').lower()

        search = self.__call__( '__values@%s__'%safename, 
                                [( 'xnat:subjectData/SUBJECT_ID', 'LIKE', '%')]
                              )

        jtable = search.get_table('xnat:subjectData', [field_name])

        if jtable.has_header(field_name.split('/')[1].lower()):
            values = jtable.get_column(field_name.split('/')[1].lower())
        else:
            values = jtable.get_column(safename)

        values = [str(val) for val in set(values)]
        values.sort()

        return values

    def _readcache(self):
        q = {}        
        t = {}
        
        cachepattern = httplib2.safename("%s/REST/search/*?format=json" % \
                                      self._interface._server).rsplit(',', 1)[0]

        excludepattern = \
            httplib2.safename("%s/REST/search/elements?format=json" % \
                              self._interface._server).rsplit(',', 1)[0]

        cachefiles = glob.glob(os.path.join(self._cachedir, cachepattern + '*'))
        excluded = glob.glob(os.path.join(self._cachedir, excludepattern + '*'))

        for cachefile in set(cachefiles).difference(excluded):
            key = cachefile.split(',')[cachefile.split(',').index('search')+1]
            if key != 'elements':
                buf = ''
                fd = open(cachefile, 'rb')
                while len(buf) < 4 or buf[-4:] != '\r\n\r\n':
                    buf += fd.read(1)
                pos = fd.tell()
                fd.seek(0)
                cached_value = fd.read(pos-4)
                info = httplib2.email.message_from_string(cached_value)
                q[key] = eval(info.get('query'))
                t.setdefault(key, []).append((info.get('row_type'), 
                                              eval(info.get('columns')))
                                            ) 

        return q, t

    def names(self):
        """ Returns the list of the saved queries names.
        """
        return [key for key in self.queries().keys() 
                if not fnmatch(key, '__values@*__')]

    def queries(self):
        """ Returns the dictionnary of the saved queries contraints. {name:query}
        """
        return self._readcache()[0]

    def tables(self):
        """ Returns the dictionnary of the saved queries returned data.
            {name:[columns]}
        """
        return self._readcache()[1]

    def get(self, name):
        """ Get saved query by name.
        """
        return Search(name, self.queries()[name], self._interface)

    def delete(self, name):
        """ Delete saved query by name.
        """
        cachepattern = httplib2.safename("%s/REST/search/%s*?format=json" % \
                              (self._interface._server, name)).rsplit(',', 1)[0]

        cachefiles = glob.glob(os.path.join(self._cachedir, cachepattern + '*'))

        for cachefile in cachefiles:
            os.remove(cachefile)


class Search(object):
    def __init__(self, name, query, interface):
        self._query = query
        self._interface = interface

        self.name = name

    def get_tests(self, row_type, test_types, additional_columns=[]):
        return self.get_table(row_type, 
                              ['%s/%s'%(test_type, field_name)
                               for test_type in test_types
                               for field_name in \
                               self._interface.search.type_fields(test_type)
                               ] + additional_columns
                              )
        
    def get_table(self, row_type, columns=[]):
        """ Submits the defined search and returns a table.

            Parameters
            ----------
            row_type: string
                The returned table will have one line for every matching
                occurence of this type. 

                e.g. xnat:subjectData/SUBJECT_ID

            columns: list of strings
                The returned table will have all the given columns.
                The valid columns names are found through the ``types()``
                and ``type_fields()`` methods of :class:`SearchManager`.

            Returns
            -------
            A JsonTable object containing the results.
        """

        start = time.time()

        full_table = JsonTable(self._interface._engine.submit_search(
                               self.name,row_type, columns, self._query))

        subtable_headers = \
            [ column.split('/')[1].lower()
              if full_table.has_header(column.split('/')[1].lower())
              else column.replace(':', '_').replace('/', '_').lower()
              for column in columns
            ]

#        print '%s results in %s seconds'%(len(full_table), time.time() - start)

        return full_table.fget_subtable(subtable_headers)

    def get_subjects(self):
        """ Returns a list of :class:`Subject` objects matching the query 
            constraints.
        """

        return restapi.CollectionObject(
               [restapi.Subject(('/REST/projects/%s'
                                 '/subjects/%s' 
                                 ) % (ids['project'], ids['subject_id']),
                                  self._interface,
                                  check_id=False
                                ) 
                for ids in self.get_table('xnat:subjectData', 
                                          ['xnat:subjectData/PROJECT', 
                                           'xnat:subjectData/SUBJECT_ID'
                                           ])
                ])

    def get_subjects_tests(self, test_types, additional_columns=[]):
        columns = ['xnat:subjectData/PROJECT', 'xnat:subjectData/SUBJECT_ID'] \
                + [field
                   for test_type in test_types
                   for field in \
                   self._interface.search.type_fields(test_type, True)
                   if not 'PROJECT' in field and not 'SUBJECT_ID' in field] \
                + additional_columns

        return self.get_table('xnat:subjectData', columns)

    def get_experiments(self, experiment_type='xnat:mrSessionData'):
        """ Returns a list of :class:`Experiment` objects matching the query
            constraints.
        """
        return restapi.CollectionObject(
               [ restapi.Experiment( ( '/REST/projects/%s'
                                       '/subjects/%s'
                                       '/experiments/%s'
                                     ) % ( ids['project'], 
                                           ids['subject_id'],
                                           ids['session_id']
                                         ),
                                     self._interface,
                                     check_id=False
                                   )
                 for ids in self.get_table( experiment_type, 
                                            [ experiment_type + '/PROJECT', 
                                              experiment_type + '/SUBJECT_ID', 
                                              experiment_type + '/SESSION_ID'
                                            ]
                                          )
               ]
            )

