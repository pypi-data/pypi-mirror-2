Introduction
============
This is a XUpdate Generator to compare any XML document.

See <http://xmldb-org.sourceforge.net/xupdate/> for information on
XUpdate.

Installation
============
python setup install

Test
====
python setup test

Usage
=====
Once you have installed erp5diff, you can use "erp5diff" in a shell::

  erp5diff old.xml new.xml


Or in a python console::

  from ERP5Diff import ERP5Diff
  erp5diff = ERP5Diff()
  old_xml = """
  <ul>
    <li>1</li>
    <li>2</li>
    <li>3</li>
    <li>4</li>
    <li>5</li>
    <li>6</li>
    <li>7</li>
    <li>8</li>
    <li>9</li>
  </ul>
  """
  new_xml = """
  <ul>
    <li>5</li>
    <li>6</li>
    <li>1</li>
    <li>2</li>
    <li>3</li>
    <li>4</li>
    <li>7</li>
    <li>8</li>
    <li>9</li>
  </ul>
  """
  erp5diff.compare(old_xml, new_xml)
  erp5diff.output()
  <xupdate:modifications xmlns:xupdate="http://www.xmldb.org/xupdate" version="1.0">
    <xupdate:remove select="/ul/li[5]"/>
    <xupdate:remove select="/ul/li[6]"/>
    <xupdate:append child="first()">
      <xupdate:element name="li">5</xupdate:element>
      <xupdate:element name="li">6</xupdate:element>
    </xupdate:append>
  </xupdate:modifications>




- 2003-12-04, Yoshinori OKUJI <yo@nexedi.com>
- 2009-09-15, Tatuya Kamada <tatuya@nexedi.com>
- 2009-2011, Nicolas Delaby <nicolas@nexedi.com>
