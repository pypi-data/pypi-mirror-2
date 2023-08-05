#!/usr/bin/python
# coding: utf-8 -*-
"""
"""
__version__ = '0.1.1'
__author__ = 'Juha Mustonen'
__email__ = 'juha.p.mustonen@gmail.com'
__license__ = 'MIT'
__import__('pkg_resources').declare_namespace(__name__)

import exceptions
from xml.etree import ElementTree

from fabric.api import env
from fabric.contrib.xfiles import reader

def query(path, xquery, fail_on_error=True):
  '''
  Makes query to remote XML file
  and returns the matching entries back

  path
    Path to remote XML document
  
  xquery
    XQuery -like selection for the elements/values in the XML document.
    Selection format:

    .. code-block:: bash

      path/to/elements            # <-- matches to elements -element
      /root/path/to/elements      # <-- absolute selection example
      path/to=value               # <-- matches with 'to' element when having text 'value' in it
      path/to=val*                # <-- matches with 'to' element when having text starting with 'val'
      path/to/elements[id]        # <-- matches to all elements having 'id' attribute
      path/to/elements[@id]       # <-- same as above
      path/to/elements[i?]        # <-- matches to all attributes with 'i'+something
      path/to/elements[i*]        # <-- matches to all attributes with 'i'
      path/to/elements[id=value]  # <-- matches to all elements having 'id' attribute with value 'value'
      path/to/elements[@id=value] # <-- same as above
      path/to/elements[id=val*]   # <-- matches to all elements having 'val'+something
      path/to/elements[i?=val*]   # <-- combination from above
      path/to[i?=val*]=val*       # <-- combination from all of the above

    .. NOTE::

       Wildcard **are not supported** for paths - at least not yet.
       So, for example, following **is not supported**::

          path/to/elem*

  fail_on_error (default True)
    If the document reading/parsing fails, an exception is raised.
    However, if this flag is set to False, and empty list is returned
    instead - silently.

  returns
    List of ElementTree -elements. Or empty list if silent fail flag
    is set

  .. code-block:: python

    # fabfile.py
    from fabric.contrib import xfiles

    def mycommand():
      for elem in xfiles.query('path/to/remotedoc.xml', 'items/item'):
        print elem.text, elem.attrib

  And to run fabfile::

    fab mycommand
  '''
  try:
    rxmlr = reader.RXMLReader().open(path)
    return rxmlr.query(xquery)
  except exceptions.Exception as er:
    if not fail_on_error:
      return []
    raise

def pprint(path, xquery):
  '''
  Prints the matching entries (whereas :meth:`query`
  only returns elements)

  .. code-block:: python

    # fabfile.py
    from fabric.contrib import xfiles

    def mycommand(rpath):
      """
      Lists the elements of remote document.
      """
      xfiles.pprint(rpath, 'items/item[attr=value]')

  And to run fabfile::

    fab mycommand:document.xml

  '''
  host = getattr(env, 'host_string', 'undefined')
  print '[%s] %s' % (host, path)

  for entry in query(path, xquery):
    print '  %s' % ElementTree.tostring(entry, 'utf-8').strip()

