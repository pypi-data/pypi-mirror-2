#!/usr/bin/python
# coding: utf-8 -*-
"""
:copyright: Copyright 2009 by Juha Mustonen, see AUTHORS.
:license: MIT, see LICENSE for details.
"""
import re
from fnmatch import fnmatch
import os
import tempfile
import shutil
from xml.etree import ElementTree

from fabric import api as fapi

class RXMLReader(object):
  '''
  XMLReader for remote files, using
  Fabric

  .. code-block:: python

    from fabric.contrib.xfiles import reader
    rxr = reader.RXMLReader()
    rxr.open('/tmp/document.xml')
    rxr.query('/root/path/items')
    # do something with the result set
    rxr.close()

  '''
  def __init__(self):
    super(RXMLReader, self).__init__()
    self.etree = None
    self.lpath = None

  def open(self, rpath):
    '''
    Reads the XML document from remote
    location and stores the parsed document
    into ``self.etree``

    rpath
      Path in server, to remote XML file
    returns
      Object itself
    '''
    # Get remote file to tmp location
    # and parse the file to etree object
    self.lpath = self._get(rpath)
    et = ElementTree.ElementTree()
    self.etree = et.parse(self.lpath)

    return self


  def query(self, query):
    '''
    Makes a query to retrived XML file.

    query
      A simple XML query to the document.

    returns
      A list of :mod:`xml.etree.ElementTree` elements that matches with the query
    '''
    onlyroot = False
    path = None
    sel_name = None
    sel_value = None
    sel_text = None

    values = []
    query = query.strip()

    # ElementTree does not like absolute paths,
    # so strip the first element if absolute path is given
    if query.startswith('/'):
      org_query = query

      # If query is like: /root/element
      if query.rfind('/') > 1:
        rootx = re.compile('^\/\w*\/*')
        query = rootx.sub('', query, 1)
      # If query is only: /root
      # set flag onlyroot for iterator
      else:
        onlyroot = True
        query = query[1:]


    #print '=== query: ', query

    # Parse query, if it contains attribute selectors
    # like:
    #   /root/element[@id]          <- attribute exists
    #   /root/element[@id=foobar]   <- attribute value matches
    #   name[id]
    #   name[@id]
    #   name[@id=value]
    #   name[@id=val*]
    #   name=value
    #   name=val*
    #   name[@id=val*]=valu?
    rflags=re.VERBOSE|re.UNICODE|re.IGNORECASE

    # TODO: split the lines
    atrx = re.compile(r'(?P<path>(\w|\/)+)(\[@?(?P<name>(\w|\*|-|\?)+)(=(?P<value>.*(?=\])))?\])?(=(?P<text>.*))?', rflags)

    # Use regexp to split the elements
    m = atrx.search(query)
    if m:
      gd = m.groupdict()
      path = gd.get('path', None)
      sel_name = gd.get('name', None)
      sel_value = gd.get('value', None)
      sel_text = gd.get('text', None)

    if not path:
      raise Exception('Regexp matching failed, check the format')

    #print '#'*20
    #print 'path: ', path, ' name: ', sel_name, ' value: ', sel_value, ' text: ', sel_text

    if self.etree is not None:
      
      # Get sub elements based on given path
      elems = self.etree.findall(path)

      # NOTE: if paths is actually a root element (/path), the outcome
      # of above is empty.
      if onlyroot:
        elems = self.etree.getiterator()

      for elem in elems:
        # If element value (text) selector is given
        if sel_text:
          # If no match, skip
          if not fnmatch(elem.text, sel_text):
            break

        # If attribute name is given in selector, ensure
        # the attribute exists
        if sel_name:
          # Check the attribute name matches with wildcard selection
          if [sel_name for k in elem.keys() if fnmatch(k, sel_name)]:
            # If value is also given check it as well
            if sel_value:

              # Because the key can match with multiple, iterate them
              # all
              for attr in elem.keys():
                if fnmatch(attr, sel_name):
                  if fnmatch(elem.get(attr), sel_value):
                    values.append(elem)

            # If only name is given
            else:
              values.append(elem)

        # No attribute selector
        else:
          values.append(elem)

    return values


  def close(self):
    '''
    Closes the reader.
    Deletes the local, temporary XML document
    '''
    if self.lpath:
      os.remove(self.lpath)


  def _get(self, rpath):
    '''
    Retrieves the remote file based on given
    remotepath ``rpath`` to local, temporary location.

    .. NOTE:: The temp file needs to be removed manually

    rpath
      Path to XML file in remote server
    returns
      Absolute path to local, temporary file
    '''
    # Create tmp file and retrieve the remote XML
    # file to it
    (fd, lpath) = tempfile.mkstemp(suffix='xfiles')

    # NOTE: special case for 'localhost' - no need to go via SSH
    # also, if host is not defined, expect it to localhost 
    # TODO: add info log from above
    if not fapi.env.host_string or fapi.env.host_string.lower() in ('localhost', '127.0.0.1'):
      shutil.copy(os.path.abspath(rpath), lpath)
    else:
      fapi.get(rpath, lpath)

    # NOTE: with Fabric 0.9, the module always adds host name
    # in the end, if multiple hosts in question. Use set to get unique listing
    if len(set(fapi.env.hosts)) > 1:
      lpath = '%s.%s' % (lpath, fapi.env.host_string)

    return lpath

