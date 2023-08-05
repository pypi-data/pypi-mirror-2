import os
import sys
import mimetypes
import httplib2
import shutil
import time
import hashlib
import tempfile
import mmap
from configobj import ConfigObj
from lxml import etree

import search
import uriutils
from jsontable import JsonTable
from cachemanager import CacheManager

# load externals if necessary
if int(sys.version[:5].replace('.', '')) < 260:
    from deque import Deque as deque
else:
    from collections import deque

try:
    import json
except:
    import simplejson as json


module_path = os.path.dirname(os.path.abspath(__file__))

try:
    cfg_dir = \
        os.path.join(os.path.expanduser('~'), '.pyxnat') \
        if not 'win' in sys.platform \
        else os.path.join(os.path.expanduser('~'), 'pyxnat')

    shortcuts_path = os.path.join(cfg_dir, 'xnat_shortcuts.cfg')

    if not os.path.exists(cfg_dir):
        os.makedirs(cfg_dir)

    if not os.path.exists(shortcuts_path):
        shutil.copyfile( os.path.join(module_path, 'xnat_shortcuts.cfg'),
                         shortcuts_path
                       )
except:
    shortcuts_path = os.path.join(module_path, 'xnat_shortcuts.cfg')

xtype_path = os.path.join(module_path, 'xtype.cfg')

_shortcuts = ConfigObj(shortcuts_path)
_xtypes = ConfigObj(xtype_path)

# --------------------------------------------------------------------------- #

class Engine(object):
    """ Class that handles the actual queries on the XNAT server.

        .. note::
            The class uses the built-in httplib2 cache system.
            It adds a time (default 3 seconds) to speed up chatty queries.
    """

    def __init__(self, server, user, password, datastore, interface):
        self._server = server

        self._stdin = deque([], 10)
        self._stdout = deque([], 10)
        self._stderr = deque([], 10)

        self._interface = interface

        if not datastore:
            datastore = tempfile.gettempdir()

        datastore = os.path.join(datastore, '%s@%s'%(user, 
                                 server.split('//')[1].replace('/', '_')))

        self._h = httplib2.Http(datastore, timeout=10)
        self._h.add_credentials(user, password)
        self._timer = {}
        self._cachedir = self._h.cache.cache
        
        self.lifetime = 3

    def _exec(self, uri, method, body=None, headers=None):
        """ Executes a query on the XNAT server.

            Parameters
            ----------
            uri: string
                This is mainly the identifier of the resource that is being
                queried. More complex queries may also need a query string
                (separated by a '?') and may need some reference to local
                resources.
            method: PUT or POST or GET or DELETE
                HTTP method
            body: string
                HTTP body
            header:
                HTTP headers

            Returns
            -------
            Result as a string.

            Examples::

            +---------+-------------------------------------------------+
            | Method  | URI                                             |
            +=========+=================================================+
            | GET     | /REST/projects?format=json                      |
            +-----------------------------------------------------------+
        """
        self._stdin.append((uri, method))

        url = self._server + uri
        cachefile = os.path.join(self._h.cache.cache, httplib2.safename(url))
        iscached = os.path.exists(cachefile) and not method in ['PUT', 'DELETE']

        fromcache = False
        if iscached:
            if (time.time() - self._timer.get(url, 0) < self.lifetime \
                or self.lifetime == 0):
                
                print 'Use L1 cache'
                cached_value = open(cachefile, 'rb').read()
                try:
                    content = cached_value.split('\r\n\r\n', 1)[1]
                except IndexError:
                    self._h.cache.delete(url)
                fromcache = True
                
        if not fromcache and not self._interface.is_offline():
            response, content = self._h.request(url, method, body, headers)
            self._timer[url] = time.time()
            if response.fromcache:
                print 'Use L2 cache'
            else:
                print 'Make request'

            try:
                assert response.status in [200, 206, 304]
            except:
                raise Exception('HttpError %s: %s'%
                                (response.status, response.reason))

        if not fromcache and self._interface.is_offline():
            raise Warning('Resource not in cache. You have to go back online '
                          'to retrieve it.')

        self._stdout.append(content)

        return content

    def get_json(self, uri):
        """ Executes a 'GET' query that answers in the json format.
        """
        return self._exec(uri+'?format=json', 'GET')

    def get_xml(self, uri):
        """ Executes a 'GET' query that answers in the xml format.
        """
        return self._exec(uri+'?format=xml', 'GET')

    def get_file(self, uri):
        """ Executes a 'GET' query on a file resource. The file content
            is saved in the local cache.

            Returns
            -------
            A file-object.
        """
        url = self._server + uri
        cachefile = os.path.join(self._h.cache.cache, httplib2.safename(url))
        
        content = self._exec(uri, 'GET')

        if os.path.exists(cachefile):
            buf = ''
            fd = os.fdopen(os.open(cachefile, os.O_RDONLY))
            while len(buf) < 4 or buf[-4:] != '\r\n\r\n':
                buf += fd.read(1)
            return fd

    def put_resource(self, uri):
        """ Executes a 'PUT' statement to create a new resource on the server.
        """
        self._exec(uri, 'PUT')

    def put_file(self, uri, filename):
        """ Executes a 'PUT' statement to put a new file on the server.

            .. note::
               The file content is passed through the body of the HTTP message.

            See also
            --------
            Engine.put_resource()
        """

        BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
        CRLF = '\r\n'
        L = []
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % 
                                        (os.path.basename(filename), filename))
        L.append('Content-Type: %s' % 
                mimetypes.guess_type(filename)[0] or 'application/octet-stream')
        L.append('')
        L.append(open(filename, 'rb').read())
        L.append('--' + BOUNDARY + '--')
        L.append('')
        body = CRLF.join(L)
        content_type = 'multipart/form-data; boundary=%s' % BOUNDARY

        self._exec(uri, 'PUT', body, headers={'content-type':content_type})

    def del_resource(self, uri):
        """ Executes a 'DELETE' statement to delete a resource on the server.
        """
        self._exec(uri, 'DELETE')

    def submit_search(self, search_name, row_type, columns, query):
        """ 'POST' an xml containing the description of a complex search.

            A complex search is composed of:
                - a series of constraints
                - a description of the data that is to be returned

            See also
            -------- 
            Search and SearchManager objects.
        """
        if self._interface.search.queries().has_key(search_name) \
        and self._interface.search.queries().get(search_name) != query:        
            self._interface.search.delete(search_name)

        key = "%s/REST/search/%s?format=json"%(self._server, search_name)

        xmldoc = search.build_search_document(row_type, columns, query)

        basename = httplib2.safename(key).replace(
                                            hashlib.md5(key).hexdigest(),
                                            hashlib.md5(xmldoc).hexdigest()
                                            )

        cachefile = os.path.join(self._h.cache.cache, basename)
        iscached = os.path.exists(cachefile)

        if iscached \
        and (time.time() - self._timer.get(basename, 0) < self.lifetime \
             or self.lifetime == 0):
            cached_value = open(cachefile, 'rb').read()
            content = cached_value.split('\r\n\r\n', 1)[1]
        else:
            content = self._exec("/REST/search?format=json", 'POST', xmldoc)
            
            if os.path.exists(cachefile):
                os.remove(cachefile)

            fd = open(cachefile, 'w')
            fd.write('search_name: %s\r\n'%search_name)
            fd.write('row_type: %s\r\n'%row_type)
            fd.write('columns: %s\r\n'%columns)
            fd.write('query: %s\r\n'%query)
            fd.write('\r\n')
            fd.write(content)
            fd.close()
            
            self._timer[basename] = time.time()

        return content

# --------------------------------------------------------------------------- #

def get_collection_object(child_resource):
    """ Used in the XType metaclass to generate a method that returns a list
        of children resource identifiers.
    """
    def sub_func(self, id_filter='*'):
        """
            Parameters
            ----------
            id_filter: string
                Filters the identifiers list according to the given pattern.
        """
        id_header = _xtypes[child_resource]['id']
        results = self._interface._engine.get_json( '%s/%ss' % \
                                                     (self._uri, child_resource)
                                                  )

        return CollectionObject(
                [self._interface.request(
                     self._uri+'/%ss/%s'%(child_resource, ID), False)
                 for ID in JsonTable(results).get_column(id_header, id_filter)
                ])

    return sub_func

def get_resource_object(child_resource):
    """ Used in the XType metaclass to generate a method that returns 
        the :class:`ResourceObject` for the specified resource.
    """
    def sub_func(self, ID):
        """
            Parameters
            ----------
            ID: string
                Identifier of the resource.
        """
        return self._interface.request(self._uri+'/%ss/%s'%(child_resource, ID))

    return sub_func


class XType(type):
    """ The ResourceObjects share a common interface for management 
        (e.g. create). They need a specialized one for listing their children
        resources since it is resource level dependent.

        This metaclass provides a way to create dynamically an accessor
        interface for the resource children on basing itself on a description
        of the resources in a configuration file ('xtype.cfg').

        Two methods are created for each resource child:
            get_resource_object(ID):
                returns the ResourceObject for that resource.

            get_collection_object(id_filter):
                returns a CollectionObject that contains the resource children.

        .. note::
            A Subject object will have the following generated methods:
                - experiment & experiments
                - resource & resources
                - file & files
    """
    def __new__(cls, name, bases, dct):
        for child_rsc in _xtypes[name.lower()]['children']:

            dct[child_rsc+'s'] = get_collection_object(child_rsc)
            dct[child_rsc] = get_resource_object(child_rsc)

        return type.__new__(cls, name, bases, dct)

    def __init__(cls, name, bases, dct):
        super(XType, cls).__init__(name, bases, dct)
        

class ResourceObject(object):
    """ All REST resources objects are derived from ResourceObject which 
        contains the common mechanisms to read and write on the server.
    """
    def __init__(self, uri, interface, check_id=True):
        """
            Parameters
            ----------
            uri: string
                Uniform Resource Identifier
            interface: :class:`Interface`
                It contains the necessary information and mechanisms to query
                the database.
            check_id: True or False
                The resource `id` may be a custom label or the actual unique id.
                The uri of a :class:`ResourceObject` must always contain the
                real id. 
                Setting this parameter to True ensures this by making a query 
                on the server. 
                Setting it to False skips this step.
        """
        self._uri = uriutils.strip_qr(uri)
        self._interface = interface

        if check_id and uriutils.get_id(uri) == self.label():
            self._uri = uriutils.join(uriutils.strip_id(uri), self.id())

#        if check_id:
#            self._uri = self.__getcell__('URI')

        self.cache = CacheManager(self)

    def __eq__(self, y):
        return self._uri == y._uri

    def __repr__(self):
        return '<%s %s>'%(self.__class__.__name__, uriutils.get_id(self._uri))

    def __getcell__(self, col_name):
        if self.exists():
            used_id = uriutils.get_id(self._uri)
            parent_uri = uriutils.strip_id(self._uri)

            jtable = JsonTable(self._interface._engine.get_json(parent_uri))

            return jtable.vfilter([used_id]).get_column(col_name)[0]

    def level(self):
        """ Returns the level of the resource corresponding to this object.
            e.g. 'project', 'subject' etc...            
        """
        return self.__class__.__name__.lower()

    def id(self):
        """ It depends on the resource, but some resources may be accessed
            through their id or through their label. The method returns the
            actual id of the resource.
        """
        id_header = _xtypes[self.level()]['id']

        return self.__getcell__(id_header)

    def label(self):
        """ It depends on the resource, but some resources may be accessed
            through their id or through their label. The method returns the
            actual label of the resource if available. If not, it will return
            a valid id.
        """
        label_header = _xtypes[self.level()]['label']

        return self.__getcell__(label_header)

    def xsi_type(self):
        """ Returns the ``xnat_type`` or ``xsi_type``which is defined in 
            the XNAT schema of this ``ResourceObject``.

            .. note:

            +----------------+-----------------------+
            | ResourceObject | possible xsi types    |
            +================+=======================+
            | Project        | xnat:projectData      |
            +----------------+-----------------------+
            | Subject        | xnat:subjectData      |
            +----------------+-----------------------+
            | Experiment     | xnat:mrSessionData    | 
            |                | xnat:petSessionData   | 
            +----------------+-----------------------+
        """
        return self.__getcell__('xsiType')

    def exists(self):
        """ Test whether this object actually exists.

            Returns
            -------
            True or False
        """
        parent_uri = uriutils.strip_id(self._uri)
        used_id = uriutils.get_id(self._uri)

        return JsonTable(self._interface._engine.get_json(parent_uri)
                        ).vfilter([used_id]) != []

    def create(self, xsi_type=None):
        """ Creates the corresponding element on the XNAT server.

            .. note::
                The xsi_type is defined in the XNAT XML Schema. It allows
                a generic type such as ``xnat:experimentData`` to be derived in
                ``xnat:mrSessionData`` and ``xnat:petSessionData`` to be given
                some specific attributes.

            Parameters
            ----------
            xsi_type: string or None
                If not None, it will affect the given schema type to the created
                element. If None, a default schema type is given, depending on
                the object type.

            See also
            --------
            ResourceObject.xsi_type()
        """
        create_uri = self._uri if xnat_type is None \
                               else self._uri + '?xsiType=%s' % xsi_type

        self._interface._engine.put_resource(create_uri)

        return self

    def delete(self, delete_files=True):
        """ Deletes the corresponding resource on the XNAT server.

            Parameters
            ----------
            delete_files: True or False
                Files attached to the resource may be kept or not on the server
                when the object is deleted. Defaults to True.
        """
        delete_uri = \
            self._uri if not delete_files else self._uri + '?removeFiles=true'

        return self._interface._engine.del_resource(delete_uri)

class CollectionObject(object):
    """ A :class:`CollectionObject` provides a collection of 
        :class:`ResourceObject`.

        It is mainly useful because it is iterable and enables the following
        behaviour::
            >>> for p in interface.projects():
            >>>     print p.subjects()

        Specific elements in the collection can be accessed either by their
        ID or by their index in the corresponding list::
            >>> projects = interface.projects()
            >>> print projects
            ['A', 'B', 'C']
            >>> projects[1] == projects['B']
            True
    """
    def __init__(self, resource_objects=[]):
        self._lst = resource_objects
        self._items = []

    def __len__(self):
        return len(self._lst)

#    def __eq__(self, y):
#        return self._lst == y._lst

    def __getitem__(self, y):
        if isinstance(y, int):
            return self._lst[y]
        elif isinstance(y, (str, unicode)):
            return dict(self.__items__())[y]

    def __getslice__(self, i, j):
        return self._lst[i:j]

    def __repr__(self):
        return repr(self.id_list())

    def __str__(self):
        return str(self.id_list())

    def __contains__(self, y):
        if isinstance(y, (str, unicode)):
            return y in self.__repr__()
        return y in self._lst

    def __iter__(self):
        return iter(self._lst)

    def __items__(self):
        if self._items == []:
            self._items = [(uriutils.get_id(rsc._uri), rsc) for rsc in self._lst]
        return self._items

    def id_list(self):
        
        return [t[0] for t in self.__items__()]

# --------------------------------------------------------------------------- #

class Interface(object):
    """ Class that holds the properties to access a XNAT server.

        >>> interface = Interface( server='http://central.xnat.org:8080',
                                   user='login',
                                   password='pwd',
                                   datastore='/tmp'
                                 )
    """
    __metaclass__ = XType

    def __init__(self, server, user, password, datastore=None, mode='online'):
        """
            Parameters
            ----------
            server: string
                The full server URL, including the port if necessary.
            user: string   
                A valid login registered through the XNAT web interface.
            password: string
                The user's password.
            datastore: string or None
                The path of the base directory to use as a data store. If
                None is given a temporary directory will be created and used
                but the cache will not be persistent.
            mode: online | offline | mixed
                online: reads the HTTP headers to decide whether to use the cache
                        or not.
                offline: only uses the cache. Raises Warning if resource not in
                         cache.
                mixed: always uses cache. If resource not cached attempt to
                        fetch it.
        """                            
        self._uri = '/REST'
        self._interface = self

        self._user = user
        self._server = server
        self._engine = Engine(server, user, password, datastore, self)
        self.cache = CacheManager(self)
        self.search = search.SearchManager(self)

        if not mode in ['online', 'offline', 'mixed']:
            mode = 'online'
        self._mode = mode
        getattr(self, 'set_%s'%mode)()

    def request(self, uri, check_id=True):
        """ Utility method to enter a REST compliant URI and get back
            the relevant ResourceObject.
        """
        if uri == '/REST':
            return self
        elif uriutils.is_resource(uri):
            try:
                return globals()[uriutils.level(uri, False).capitalize()] \
                                                    (uri, self, check_id)
            except TypeError:
                return globals()[uriutils.level(uri, False).capitalize()] \
                                                        (uri, self)
        elif uriutils.level(uri) in ['input', 'output']:
                return Container(uri, self)
        elif uriutils.is_query(uri):
            return getattr(self.request(uriutils.parent(uri), check_id),
                           uriutils.level(uri, True))()

    def set_offline(self):
        self._engine.backup_lifetime = self._engine.lifetime
        self._engine.lifetime = 0
        self._mode = 'offline'

    def set_online(self):
        try:
            self._engine.lifetime = self._engine._backup_lifetime
        except:
            self._engine.lifetime = 3

        self._mode = 'online'

    def set_mixed(self):
        self._engine.backup_lifetime = self._engine.lifetime
        self._engine.lifetime = 0
        self._mode = 'mixed'

    def is_offline(self):
        return self._mode == 'offline'

    def is_online(self):
        return self._mode == 'online'

    def is_mixed(self):
        return self._mode == 'mixed'


class Project(ResourceObject):
    """ Specialized ResourceObject class for projects.
    """
    __metaclass__ = XType

    def __init__(self, uri, interface, check_id=True):
        ResourceObject.__init__(self, uri, interface, check_id)
        self.attrib = Attrib(self)

    def xsi_type(self):
        return 'xnat:projectData'


class Subject(ResourceObject):
    """ Specialized ResourceObject class for subjects.
    """
    __metaclass__ = XType

    def __init__(self, uri, interface, check_id=True):
        ResourceObject.__init__(self, uri, interface, check_id)
        self.attrib = Attrib(self)

    def xsi_type(self):
        return 'xnat:subjectData'


class Experiment(ResourceObject):
    """ Specialized ResourceObject class for experiments.
    """
    __metaclass__ = XType

    def __init__(self, uri, interface, check_id=True):
        ResourceObject.__init__(self, uri, interface, check_id)
        self.attrib = Attrib(self)

    def create(self, xnat_type='xnat:mrSessionData'):
        return super(Experiment, self).create(xnat_type)


class Scan(ResourceObject):
    """ Specialized ResourceObject class for scans.
    """
    __metaclass__ = XType

    def __init__(self, uri, interface, check_id=True):
        ResourceObject.__init__(self, uri, interface, check_id)
        self.attrib = Attrib(self)

    def create(self, xnat_type='xnat:mrScanData'):
        return super(Scan, self).create(xnat_type)

#    def type(self):
#        return self.__getcell__('type')

#    def quality(self):
#        return self.__getcell__('quality')

#    def series_description(self):
#        return self.__getcell__('series_description')

class Reconstruction(ResourceObject):
    """ Specialized ResourceObject class for reconstructions.
    """
    def __init__(self, uri, interface, check_id=True):
        ResourceObject.__init__(self, uri, interface, check_id)
        self.attrib = Attrib(self)

        self.inputs = Container(uriutils.join(self._uri, 'in'), interface)
        self.outputs = Container(uriutils.join(self._uri, 'out'), interface)


class Assessor(ResourceObject):
    """ Specialized ResourceObject class for assessors.
    """
    def __init__(self, uri, interface, check_id=True):
        ResourceObject.__init__(self, uri, interface, check_id)
        self.attrib = Attrib(self)

        self.inputs = Container(uriutils.join(self._uri, 'in'), interface)
        self.outputs = Container(uriutils.join(self._uri, 'out'), interface)


class Container(object):
    def __init__(self, uri, interface):
        self._uri = uri
        self._interface = interface
        self.cache = CacheManager(self)

    def __call__(self, *args, **kwargs):
        return self

    def __iter__(self):
        yield self

    def __collection__(self, rsc, id_filter):
        id_header = _xtypes[rsc]['id']
        uri = uriutils.join(self._uri, rsc+'s')
        jtable = JsonTable(self._interface._engine.get_json(uri))

        return CollectionObject(
                [self._interface.request(self._uri+'/%ss/%s'%(rsc, ID), False)
                 for ID in jtable.get_column(id_header, id_filter)
                ])

    def __resource__(self, rsc, rsc_id):
        return self._interface.request(
                    uriutils.join(self._uri ,rsc+'s', rsc_id))

    def files(self, id_filter='*'):
        return self.__collection__('file', id_filter)

    def file(self, filename):
        return self.__resource__('file', filename)

    def resources(self, id_filter='*'):
        return self.__collection__('resource', id_filter)

    def resource(self, rsc_id):
        return self.__resource__('resource', rsc_id)


class Resource(ResourceObject):
    """ Specialized ResourceObject class for resources.
    """
    __metaclass__ = XType

    def __init__(self, uri, interface, check_id=True):
        ResourceObject.__init__(self, uri, interface, check_id)


class File(ResourceObject):
    """ Specialized ResourceObject class for files.
    """
    __metaclass__ = XType

    def __init__(self, uri, interface):
        ResourceObject.__init__(self, uri, interface, check_id=False)
        self._is_init = False
        self._init()

    def _init(self):
        if not self._is_init and self.exists():
            self._is_init = True
            self._uri = self.__getcell__('URI')
            if self._uri.split('/')[-2] != 'files':
                i = self._uri.split('/').index('files')
                self._folder = '/'.join(self._uri.split('/')[i+1:-1])
                self._uri = '/'.join(self._uri.split('/')[:i+1] + [uriutils.get_id(self._uri)])  

    def type(self):
        return u'file'

    def size(self):
        """ 
            Returns
            -------
            The size of the file in bytes as a string.
        """
        return self.__getcell__('Size')

    def tags(self):
        """ 
            Returns
            -------
            The specified tags for this file.
        """
        return self.__getcell__('file_tags').strip('\'')

    def format(self):
        """ 
            Returns
            -------
            The specified format for this file.

            e.g. NIFTI, DICOM, jpeg, txt, csv
        """
        return self.__getcell__('file_format').strip('\'')

    def content(self):
        """ 
            Returns
            -------
            The specified content for this file.

            e.g. T1, DTI, sequence preview, table
        """
        return self.__getcell__('file_content').strip('\'')

    def resource(self):
        return Resource(uriutils.parent(self.__getcell__('URI')), self._interface)

    def get(self):
        """ Downloads the file if it is not in the local cache.

            .. note::
                The data in the cache is kept up to date using the cache HTTP
                headers. If an external program were to modify the data without
                updating the headers, the data would no longer be synchronized
                correctly. This is why the returned file descriptor is 
                read-only. Use `get_copy()` if you wish to modify the data.

            See also
            --------
            File.get_copy()

            Returns
            -------
            A read-only file descriptor.
        """
        self._init()
        if hasattr(self, '_folder'):
            i = self._uri.split('/').index('files')
            uri = '/'.join(self._uri.split('/')[:i+1] + \
                           self._folder.split('/') + \
                           self._uri.split('/')[i+1:])
        else:
            uri = self._uri

        return self._interface._engine.get_file(uri)

    def get_copy(self, dest=None):
        """ Downloads the file if it is not in the local cache and creates
            a copy.
            
            Parameters
            ----------
            dest: string | None
                Destination of the copy.
                If None, a default path within the cache directory is chosen.

            See also
            --------
            File.get()

            Returns
            -------
            The file path as a string.
        """
        self._init()
        if not dest:
            dest = os.path.join(self._interface._engine._cachedir, 
                             'workspace', *self._uri.strip('/').split('/')[1:])
            
        if not os.path.exists(os.path.dirname(dest)):
            os.makedirs(os.path.dirname(dest))

        fd = self.get()
        open(dest, 'wb').write(fd.read())
        fd.close()
        return dest

    def put(self, local_file, format='undefined', \
                  content='unknown', tags='none'):
        """ Uploads a local file on the server.

            Returns
            -------
            True if successful, False otherwise.
        """
        format = "'%s'"%format if ' ' in format else format
        content = "'%s'"%content if ' ' in content else content
        tags = "'%s'"%tags if ' ' in tags else tags

        put_uri = "%s?format=%s&content=%s&tags=%s" % \
                                            (self._uri, format, content, tags)

        self._interface._engine.put_file(put_uri, local_file)
        self._init()

    def delete(self):
        """ Removes the file from the server and from the cache if necessary.
        """
        self._init()
        print 'DELETE', self._uri
        self._interface._engine._exec(self._uri, 'DELETE')


class Attrib(object):
    """ Class that provides access to a resource metadata.

        It behaves mainly as a dictionnary that synchronizes itself with
        the server.
    """
    def __init__(self, robj):
        """
            Parameters
            ----------
            robj: ResourceObject
                The ResourceObject it is linked to.        
        """
        self._robj = robj
        self._interface = robj._interface
        self._map = _shortcuts[robj.level()]

    def __str__(self):
        return str(ConfigObj(self.as_dict()).write()
                  ).replace(', ', '\n').replace("'", ''
                  ).strip('[').strip(']')

    def __repr__(self):
        return 'Attrib(%s)' % repr(self.as_dict())

    def __getitem__(self, name):
        """ Returns the value of the specified attribute.
            Raises an exception if the attribute does not exists.

            e.g. subject.attrib['label']

            .. note::
                There is no XNAT REST method to directly get the value of a
                specific attribute so an xml file with all the data attached
                to the resource is downloaded and then parsed.
        """
        name_in_schema = self._map[name].split('/')[-1]

        xml_root = \
            etree.fromstring(
                    self._interface._engine.get_xml(self._robj._uri)
                            )

        token_xpath = ['/*']
        for token in self._map[name].split('/'):

            if ':' not in token and '[' not in token:
                token_xpath.append("*[local-name()='%s']"%token)
            elif '[' in token:
                node_name, xsi_type = token.rstrip(']').split('[')

                xsi_type = xsi_type if xsi_type[0] == '@' else '@' + xsi_type
                xsi_type = xsi_type.replace('=', '=\'') + '\''

                token_xpath.append( "*[local-name()='%s'][%s]" % \
                                    (node_name, xsi_type)
                                  )
            else:
                pass

        element = \
            xml_root.xpath( '/'.join(token_xpath),
                            namespaces=xml_root.nsmap
                          )

        attribute = \
            xml_root.xpath( '/'.join(token_xpath[:-1]) + '[@%s]' % \
                            name_in_schema,
                            namespaces=xml_root.nsmap
                          )

        # I hope xnat rest api works this way for every 'field' in 'fields'
        if token_xpath[-1] == "*[local-name()='field']":
            val = xml_root.xpath( '/'.join(token_xpath[:-1]),
                                   namespaces=xml_root.nsmap
                                )[0].getchildren()[0].tail.strip('\'')

        elif element != [] and attribute != []:
            raise Exception( ( "AttribException: path "
                               "for attribute '%s'"
                               "is ambigious, two "
                               "possible values (%s and %s)"
                             ) % ( name, 
                                   element[0].text,
                                   attribute[0].get(name_in_schema)
                                 )
                           )
        elif element != []:
            val = element[0].text.strip('\'')
        elif attribute != []:
            val = attribute[0].get(name_in_schema).strip('\'')            
        else:
            return

        # if the set value is '', it is stored with its ascii character on xnat
        if val != '39#':
            return val
        return 

    def __setitem__(self, name, val):
        """ Sets the value of the specified attribute.

            See also
            --------
            Attrib.update()
        """
        self.update({name:val})

    def as_dict(self):
        """
            Returns
            -------
            The attributes names and values as a standard python dict.
        """
        return dict(self.items())

    def get(self, name):
        """ Returns the value of the specified attribute.
            Returns None if the attribute does not exists.
        """
        if self.has_key(name):
            return self[name]

    def has_key(self, name):
        """ Test whether this resource has the specified attribute.
        """
        return name in self.keys()

    def items(self):
        """
            Returns
            -------
            The attributes names and values as a list of 2-tuples.
        """
        return zip(self.keys(), self.values())

    def keys(self):
        """ List of all the available attributes names for this resource. 
        """
        return self._map.keys()

    def set(self, name, val):
        """ Sets the value of the specified attribute.

            See also
            --------
            Attrib.update()
        """
        if self.has_key(name):
            self.update({name:val})
            return True
        return False

    def update(self, dct):
        """ Takes a dictionnay and update the attributes with its values.
            
            It is recommanded to use this method when more than one value
            has to be set because this way, they are all uploaded in a single
            shot.

            Parameters
            ----------
            dct: dict
                The dictionnary.
        """
        if dct != {}:
            for key in dct.keys():
                dct[key] = "39#" if str(dct[key]) == '' or dct[key] == None \
                                 else dct[key]

            set_values = \
                ['%s=%s'%(self._map[key], dct[key]) for key in dct.keys()]

            self._interface._engine.put_resource(
                            '%s?xsiType=%s&%s' % ( self._robj._uri,
                                                   self._robj.xsi_type(),
                                                   '&'.join(set_values)
                                                 )
                                                )

            dct.clear()
            return True
        return False

    def values(self):
        """ Returns all the values of the attributes as a list.
        """
        return [self.get(key) for key in self.keys()]


