import os
import glob
import httplib2
import shutil
from fnmatch import fnmatch
from StringIO import StringIO

from configobj import ConfigObj

import uriutils

_xtypes = ConfigObj(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                 'xtype.cfg'))

#BUFFER_SIZE = 1000000
#BUFFER_SIZE = 10

class CacheManager(object):
    """ Manual manager for the cached data.

        The cache management is mainly transparent but it is useful sometimes
        to do theses actions manually.

        A cache manager is linked to a ResourceObject and only works upon 
        the cached data related to this object.
        
        e.g. If the ResourceObject is a subject, related data may be:
                 - its files
                 - its experiments
                 - the list of subjects from its project

        The cache manager should be accessed through the `cache` attribute
        of its corresponding resource.

        >>> subject.cache(pattern='*', files=True, recursive=True)
        >>> subject.cache.clear()
    """
    def __init__(self, robj):
        """
            Parameters
            ----------
            robj: ResourceObject
                The :class:`ResourceObject` the cache manager is linked to.
        """
        self._robj = robj
        self._interface = robj._interface
        self._cachedir = self._interface._engine._cachedir

    def __call__(self, pattern='*', files=True, attrib=False):
        """ Put all the resources related to this object in the local datastore.

            Parameters
            ----------
            attrib: True or False
                Caches the objects attributes.
            files: True or False
                Downloads attached files if any.
            recursive: True or False
                Iterates through the object descendants and caches them as
                well with the same 'attrib' and 'files' parameters.
        """
        uri = self._robj._uri
        
        if '/' in pattern:
            typepat, idpat, futurepat = (pattern + '/').split('/', 2)
        else:
            typepat = '*'
            idpat = pattern
            futurepat = pattern

        for childtype in _xtypes[uriutils.level(uri)]['children']:
            if fnmatch(childtype+'s', typepat):
                try:
                    for child in getattr(self._robj, childtype+'s')(idpat):
                        print child
                        if futurepat != '':
                            child.cache(futurepat, files, attrib)
                        if childtype == 'file' and files:
                            child.get().close()
                        if hasattr(child, 'attrib') and attrib:
                            child.attrib
                except Exception, e:
                    print e

    def files(self):
        """ Returns the list of URIs of the files resources in cache.
        """
        cachename = httplib2.safename(self._interface._server + self._robj._uri
                                     ).rsplit(',', 1)[0]
        cachepattern = '%s*'%cachename
        excludepattern = '%s*?format=*'%cachename

        cached = glob.glob(os.path.join(self._cachedir, cachepattern))
        excluded = glob.glob(os.path.join(self._cachedir, excludepattern))

        return [r.rsplit(',', 1)[0].split('REST')[1].replace(',', '/')
                for r in set(cached).difference(excluded)]

    def resources(self):
        """ Returns the list of URIs of the non-files resources in cache.
        """
        cachename = httplib2.safename(self._interface._server + self._robj._uri
                                     ).rsplit(',', 1)[0]
        cachepattern = '%s*?format=*'%cachename
        excludepattern = \
            httplib2.safename("%s/REST/search/*?format=*" % \
                              self._interface._server).rsplit(',', 1)[0]

        cached = glob.glob(os.path.join(self._cachedir, cachepattern))
        excluded = glob.glob(os.path.join(self._cachedir, excludepattern))

        c = []

        for r in set(cached).difference(excluded):
            r = r.rsplit(',', 1)[0].split('REST')[1]
            uri, qs = r.rsplit(',', 1)
            c.append(uri.replace(',', '/') + '?' + qs)

        return c

    def clear(self, datatype='all'):
        """ Clears the cached data for this object.

            Parameters
            ----------
            data: 'all' | 'resources' | 'files'
                Optional parameter to delete partially the cache.
        """
        cachename = httplib2.safename(self._robj._uri).rsplit(',', 1)[0]

        if datatype == 'all':
            for cachefile in os.listdir(self._cachedir):
                if cachename in cachefile:
                    os.remove(os.path.join(self._cachedir, cachefile))
        elif datatype == 'resources':
            for cachefile in self.resources():
                if cachename in cachefile:
                    os.remove(os.path.join(self._cachedir, cachefile))       
        elif datatype == 'files':
            for cachefile in self.files():
                if cachename in cachefile:
                    os.remove(os.path.join(self._cachedir, cachefile))        
            
#class SplitCache(object):
#    """Uses a local directory as a store for cached files.
#    Not really safe to use if multiple threads or processes are going to 
#    be running on the same cache.
#    """
#    def __init__(self, cache, safe=httplib2.safename):
#        self.cache = cache
#        self.safe = safe
#        if not os.path.exists(cache):
#            os.makedirs(self.cache)

#    def read(self, safekey):
#        retval = None
#        cache_entry_path = os.path.join(self.cache, safekey)

#        if os.path.exists(cache_entry_path):
#            f = file(os.path.join(cache_entry_path, 'http.hdr'), "r")
#            retval = f.read()
#            f.close()

#            retval += '\r\n\r\n'
#            content_files = glob.glob(cache_entry_path + '/*.cache')
#            content_files.sort()

#            for content_file in content_files:
#                f = file(content_file, "r")
#                retval += f.read()
#                f.close()

#        return retval

#    def write(self, safekey, value):
#        cache_entry_path = os.path.join(self.cache, safekey)

#        if not os.path.exists(cache_entry_path):
#            os.makedirs(cache_entry_path)

#        header, content = value.split('\r\n\r\n')

#        f = file(os.path.join(cache_entry_path, 'http.hdr'), "w")
#        f.write(header)
#        f.close()

#        content = StringIO(content)

#        b = None
#        i = 0

#        while True:
#            b = content.read(BUFFER_SIZE)
#            if b == '':
#                break

#            f = file(os.path.join(cache_entry_path, '%016d.cache'%i), "w")
#            f.write(b)
#            f.close()
#            i += 1

#    def remove(self, safekey):
#        cache_entry_path = os.path.join(self.cache, safekey)
#        if os.path.exists(cache_entry_path):
#            shutil.rmtree(cache_entry_path)

#    def get(self, key):
#        return self.read(self.safe(key))

#    def set(self, key, value):
#        self.write(self.safe(key), value)

#    def delete(self, key):
#        self.remove(self.safe(key))        

#    def keys(self, pattern='*'):
#        return [os.path.split(key)[1]
#                for key in glob.glob(self.cache + '/%s'%pattern)
#                if os.path.isdir(key) and ',' in key]


