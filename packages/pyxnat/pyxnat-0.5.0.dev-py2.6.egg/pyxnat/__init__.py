""" Pyxnat is a simple python library that relies on the REST API provided
by the XNAT platform since its 1.4 version. XNAT is an extensible database for neuroimaging data. The main objective is to ease communications with an XNAT
server to plug-in external tools or python scripts to process the data. It
features:

    #. resources browsing capabilities
    #. read and write access to resources
    #. complex searches
    #. disk-caching of requested files and resources

.. [#] http://www.xnat.org/
.. [#] http://packages.python.org/pyxnat/

____

    **A short overview**    

    *Setup the connection*
        >>> from pyxnat import Interface
        >>> interface = Interface(server='http://central.xnat.org:8080',
                                  user='login',
                                  password='pass',
                                  datastore=os.path.join( os.path.expanduser('~'),
                                                          'XnatStore'
                                                        )
                                 )

    *Browse the resources*
        >>> interface.projects()
        [u'CENTRAL_OASIS_CS', u'CENTRAL_OASIS_LONG', ...]

    *Create new resources*
        >>> interface.project('my_project').create()
        >>> interface.project('my_project').file('image.nii').put('/tmp/image.nii')

    *Metadata support*
        >>> proj = interface.project('my_project')
        >>> proj.attrib.keys()
        ['note','alias','secondary_ID','name','pi_lastname',
         'label','keywords','pi_firstname','ID','description']
        >>> proj.attrib.set('note', 'a note')
        >>> proj.attrib.get('note')
        'a note'

    *Make complex searches*
        >>> search = interface.search( 'my_search',
                                       [ ('xnat:subjectData/SUBJECT_ID','LIKE','%'),
                                         ('xnat:subjectData/PROJECT', '=', 'my_project'),
                                         'AND'
                                       ]
                                     )
        >>> search.get_subjects()
"""

__version__ = '0.5.0'

import os
import sys

if os.path.join(os.path.dirname(os.path.abspath(__file__)), 'externals') \
    not in sys.path:
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                                               'externals'))

import httplib2
from .restapi import Interface, CacheManager, \
                     ResourceObject, CollectionObject, \
                     Project, Subject, Experiment, Scan, \
                     Resource, File, Attrib

from .search import SearchManager

from .restapi import shortcuts_path as xnatrest_shortcuts
from .restapi import xtype_path as xnatrest_xtype
from .restapi import _xtypes as xtypes
from .restapi import _shortcuts as shortcuts

from .jsontable import JsonTable


