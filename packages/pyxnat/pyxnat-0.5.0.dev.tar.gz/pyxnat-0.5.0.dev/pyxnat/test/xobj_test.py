import os
from configobj import ConfigObj
import tempfile

from nose import *

from pyxnat import *
import time

debug = open('debug.log', 'a')

interface = Interface( 'http://central.xnat.org',
                       'nosetests', 
                       'nosetests'
                     )

interface.cache.clear()
interface._engine.lifetime = 2

project = interface.project('nosetests')

if not project.exists():
    project.create()

subj_name = tempfile.mktemp(prefix='subj_').split(os.path.sep)[-1]

local_filename = \
        os.path.join( os.path.dirname(os.path.abspath(__file__)),
                      'test_file.txt'
                    )
remote_filename = \
    tempfile.mktemp(prefix='file_', suffix='.txt').split(os.path.sep)[-1]


def test_create_subject():
    project.subject(subj_name).create()

def test_search_types():
    assert 'xnat:subjectData' in interface.search.types()

def test_search_type_fields():
    assert 'SUBJECT_ID' in interface.search.type_fields('xnat:subjectData')

def test_search_save_get_delete():
    assert isinstance(interface.search('test_search', 
                        [
                            ('xnat:subjectData/SUBJECT_ID','LIKE','%'),
                            ('xnat:subjectData/PROJECT', '=', 'nosetests'),
                            'AND'
                        ]).get_subjects(),
                      CollectionObject
                     )

    assert 'test_search' in interface.search.names()

    interface.search.delete('test_search')
    
    assert 'test_search' not in interface.search.names()

def test_resource_listing():
    assert isinstance(interface.projects(), CollectionObject)

def test_resource_access():
    time.sleep(3)
    assert project.subject(subj_name).exists()
    assert project.subject(subj_name).attrib['label'] == \
           project.subject(subj_name).label()
    assert project.subject(subj_name).attrib['ID'] == \
           project.subject(subj_name).id()
    assert project.subject(subj_name).level() == 'subject'
    assert project.subject(subj_name).xsi_type() == 'xnat:subjectData'

def test_file_listing():
    assert isinstance(project.subject(subj_name).files(), CollectionObject)

def test_file_operations():
    f = project.subject(subj_name).file(remote_filename)
    f.put(local_filename)
    time.sleep(3)
    assert f.exists()
    assert f.size() == str(os.path.getsize(local_filename))
    assert f.size() == str(os.path.getsize(f.get_copy()))
    f.delete()
    time.sleep(3)
    assert not f.exists()

def test_resource_attrib():
    assert project.subject(subj_name).attrib.keys() == \
                ConfigObj(xnatrest_shortcuts)['subject'].keys()

def test_resource_attrib_set():
    assert project.subject(subj_name).attrib.set('height', '160')
    assert project.subject(subj_name).attrib.set('age', '15')

def test_resource_attrib_get():
    assert project.subject(subj_name).attrib.get('height') == '160.0'
    assert project.subject(subj_name).attrib.get('age') == '15'

def test_resource_attrib_get_attr():
    assert project.subject(subj_name).attrib['label'] == subj_name

def test_delete_subject():
    assert project.subject(subj_name).exists()
    project.subject(subj_name).delete()
    time.sleep(3)
    assert not project.subject(subj_name).exists()


