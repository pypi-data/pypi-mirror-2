# -*- coding: utf-8 -*-
'''
Testing module for xfiles.
Requires following external modules:

nose
  Advanced unit testing module
  http://somethingaboutorange.com/mrl/projects/nose/

fudge
  Mock solution for unit testing
  http://farmdev.com/projects/fudge/

'''

import os
import unittest
import tempfile
from xml.parsers import expat
from xml.etree import ElementTree

from fabric import api
from nose import with_setup, tools
import fudge
from utils import mock_streams

from fabric.contrib.xfiles import query, pprint, reader

dirname = os.path.dirname(__file__)

class TestRXMLReader(unittest.TestCase):
  '''
  Testcase class for testing the RXMLReader
  '''

  def setUp(self):
    '''
    Setups the test case
    '''
    # Create patch and point to local doc
    self.doc = os.path.abspath(os.path.join(dirname, 'document.xml'))

    nocopy = fudge.Fake(callable=True).with_arg_count(1).returns(self.doc)
    nodel = fudge.Fake(callable=True).returns(None)

    # Create and patch the _get function to not to use tmp folder
    self.xr = reader.RXMLReader()
    self.pxr = fudge.patch_object(reader.RXMLReader, "_get", nocopy)
    self.pxr = fudge.patch_object(reader.RXMLReader, "close", nodel)
    fudge.clear_calls()


  def tearDown(self):
    '''
    Setups the test case
    '''
    self.pxr.restore()


  def gen_doc(self):
    '''
    Generates tmp doc
    '''
    # Create tmp file to delete
    (fd, fpath) = tempfile.mkstemp(suffix='xfiles.test')
    fp = os.fdopen(fd, 'w+')
    fp.write('<root/>')
    fp.close()

    return fpath


  def get_reader(self, doc):
    '''
    Creates a faked reader using given document, relative
    to the test directory
    '''
    fdoc = os.path.abspath(os.path.join(dirname, doc))

    nocopy = fudge.Fake(callable=True).with_arg_count(1).returns(fdoc)
    nodel = fudge.Fake(callable=True).returns(None)

    self.xr = reader.RXMLReader()
    pxr = fudge.patch_object(reader.RXMLReader, "_get", nocopy)
    pxr = fudge.patch_object(reader.RXMLReader, "close", nodel)
    fudge.clear_calls()

    return self.xr


  @fudge.with_fakes
  def test_basic_query(self):
    self.xr.open(self.doc)
    tools.eq_(len(self.xr.query('elements/elem')), 2)


  @fudge.with_fakes
  @fudge.with_patched_object(reader.RXMLReader, '_get', fudge.Fake(callable=True).returns('nowhere.xml'))
  def test_nonexisting_file_noerror(self):
    tools.eq_(len(query('nowhere.xml', '/document/elements', fail_on_error=False)), 0)


  @fudge.with_fakes
  def test_nonexisting_query(self):
    self.xr.open(self.doc)
    tools.eq_(len(self.xr.query('foo')), 0)


  @fudge.with_fakes
  def test_attr_result(self):
    self.xr.open(self.doc)
    attrs = [elem.keys() for elem in self.xr.query('/document/elements/elem')]
    # two elements
    tools.eq_(len(attrs), 2)
    # one argument per element
    tools.eq_(len(attrs[0]), 1)
    tools.eq_(len(attrs[1]), 1)


  @fudge.with_fakes
  @fudge.with_patched_object(reader.RXMLReader, '_get', fudge.Fake(callable=True).returns('nowhere.xml'))
  @tools.raises(IOError)
  def test_nonexisting_file(self):
    self.xr.open('nowhere.xml')


  @fudge.with_fakes
  @fudge.with_patched_object(reader.RXMLReader, '_get', fudge.Fake(callable=True).returns('nowhere.xml'))
  @tools.raises(IOError)
  def test_nonexisting_file_query(self):
    query('nowhere.xml', '/document')


  @fudge.with_fakes
  @fudge.with_patched_object(reader.RXMLReader, '_get', fudge.Fake(callable=True).returns(os.path.join(dirname, 'invalid.xml')))
  @tools.raises(expat.ExpatError)
  def test_invalid_file(self):
    self.xr = reader.RXMLReader()
    self.xr.open('invalid.xml')


  @fudge.with_fakes
  @fudge.with_patched_object(reader.RXMLReader, '_get', fudge.Fake(callable=True).returns(gen_doc(None)))
  def test_close(self):
    xread = reader.RXMLReader()
    xread.open('gendoc')
    self.pxr.restore()
    xread.close()


  @fudge.with_fakes
  @fudge.with_patched_object(reader.RXMLReader, '_get', fudge.Fake(callable=True).returns(os.path.join(dirname, 'simple.xml')))
  def test_simple(self):
    '''
    Test the func with root-only docs
    '''
    self.xr = reader.RXMLReader()
    self.xr.open('simple.xml')

    #doc = os.path.abspath(os.path.join(dirname, 'simple.xml'))
    #self.xr.open(doc)
    #xr = self.get_reader('simple.xml')

    print 'xml:', ElementTree.tostring(self.xr.query('/simple')[0])
    # root list
    tools.eq_(len(self.xr.query('/simple')), 1)

    # root value
    tools.eq_(len(self.xr.query('/simple=textvalue')), 1)
    tools.eq_(len(self.xr.query('/simple=nonmatch')), 0)

    # id test
    tools.eq_(len(self.xr.query('/simple[id=*]')), 1)
    tools.eq_(len(self.xr.query('/simple[id=value]')), 1)
    tools.eq_(len(self.xr.query('/simple[nid]')), 0)


  @fudge.with_fakes
  def test_xfiles_query(self):
    '''
    Test the direct query, using matching 
    element
    '''
    tools.eq_(len(query('gen', 'elements/elem')), 2)


  @fudge.with_fakes
  def test_xfiles_attr_query(self):
    '''
    Test the attribute query, using matching 
    element and attribute
    '''
    # Single matching attr value
    q = 'elements/elem[@id=e1]'
    tools.eq_(len(query('gen', q)), 1)

    # Non-matching attr value
    q = 'elements/elem[@id=eX]'
    tools.eq_(len(query('gen', q)), 0)

    # Non-matching attr name
    q = 'elements/elem[foo]'
    tools.eq_(len(query('gen', q)), 0)

    # Attr name, no value
    q = 'elements/elem[@id]'
    tools.eq_(len(query('gen', q)), 2)


  @fudge.with_fakes
  def test_xfiles_attr_wildquery(self):
    '''
    Test the attribute query with wildcard selection
    '''
    # Single matching attr value
    q = 'elements/elem[@id=?1]'
    tools.eq_(len(query('gen', q)), 1)

    # Non-matching attr value
    q = 'elements/elem[@id=?e?]'
    tools.eq_(len(query('gen', q)), 0)

    # Non-matching attr name
    q = 'elements/elem[foo*]'
    tools.eq_(len(query('gen', q)), 0)

    # Attr name, no value
    q = 'elements/elem[@i*]'
    tools.eq_(len(query('gen', q)), 2)

    # Try wild card on both elements
    q = 'elements/elem[i?=e?]'
    tools.eq_(len(query('gen', q)), 2)

    q = 'elements/elem[*=??]'
    tools.eq_(len(query('gen', q)), 2)

    # Test escape
    q = 'sub[name=tes*]'
    tools.eq_(len(query('gen', q)), 3)


  @fudge.with_fakes
  def test_xfiles_elem_value(self):
    '''
    Test the elem value selection query
    '''
    # Basic value match
    q = '/document/sub[name]=subvalue'
    tools.eq_(len(query('gen', q)), 3)

    # Basic non-match test
    q = '/document/sub[name]=foovalue'
    tools.eq_(len(query('gen', q)), 0)

    # Simple value: positive test
    q = 'elements/elem=1'
    tools.eq_(len(query('gen', q)), 1)

    # Simple value: positive test with wildcard
    q = 'elements/elem=?'
    tools.eq_(len(query('gen', q)), 2)

    # Simple value: negative test
    q = 'elements/elem=3'
    tools.eq_(len(query('gen', q)), 0)

    # Combination test1
    q = '/document/sub[@nam?=*-*]=sub*'
    tools.eq_(len(query('gen', q)), 2)


  @fudge.with_fakes
  def test_xfiles_pprint(self):
    '''
    Test the direct query
    '''
    # just run xfiles pprint
    pprint('gen', 'elements/elem')

