Introduction
============

Apply xupdate diff on XML documents.


Installation
============

python setup.py install


Testing
=======

python setup.py test

Usage
=====

just like this::
  >>> from xupdate_processor import applyXUpdate
  >>> from lxml import etree
  >>> xml_doc_string = """<?xml version="1.0"?>
  <erp5>
    <object portal_type="Test">
      <title>A</title>
    </object>
    <object portal_type="Test">
      <title>A</title>
    </object>
    <object portal_type="Test">
      <title>A</title>
    </object>
  </erp5>
  """
  >>> xml_xu_string = """<?xml version="1.0"?>
  <xupdate:modifications xmlns:xupdate="http://www.xmldb.org/xupdate" version="1.0">
    <xupdate:update select="/erp5/object[2]/title">B</xupdate:update>
    <xupdate:update select="/erp5/object[3]/title">C</xupdate:update>
  </xupdate:modifications>
  """
  >>> result_tree = applyXUpdate(xml_xu_string=xml_xu_string, xml_doc_string=xml_doc_string)
  >>> print etree.tostring(result_tree, pretty_print=True)
  <erp5>
    <object portal_type="Test">
      <title>A</title>
    </object>
    <object portal_type="Test">
      <title>B</title>
    </object>
    <object portal_type="Test">
      <title>C</title>
    </object>
  </erp5>
