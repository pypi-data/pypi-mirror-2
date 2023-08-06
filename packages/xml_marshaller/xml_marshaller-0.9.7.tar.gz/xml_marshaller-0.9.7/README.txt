Introduction
============

Marshals simple Python data types into a custom XML format.
The Marshaller and Unmarshaller classes can be subclassed in order
to implement marshalling into a different XML DTD.
Original Authors are XML-SIG (xml-sig@python.org).

Fully compatible with PyXML implementation, enable namespace support for
XML Input/Output.

Implemented with lxml

Installation
============

python setup.py install


Testing
=======

python setup.py test

Usage
=====

For simple serialisation and unserialisation::


  >>> from xml_marshaller import xml_marshaller
  >>> xml_marshaller.dumps(['item1', {'key1': 1, 'key2': u'unicode string'}])
  '<marshal><list id="i2"><string>item1</string><dictionary id="i3"><string>key1</string><int>1</int><string>key2</string><unicode>unicode string</unicode></dictionary></list></marshal>'
  >>> xml_marshaller.loads(xml_marshaller.dumps(['item1', {'key1': 1, 'key2': u'unicode string'}]))
  ['item1', {'key2': u'unicode string', 'key1': 1}]

Can works with file like objects::


  >>> from xml_marshaller import xml_marshaller
  >>> from StringIO import StringIO
  >>> file_like_object = StringIO()
  >>> xml_marshaller.dump('Hello World !', file_like_object)
  >>> file_like_object.seek(0)
  >>> file_like_object.read()
  '<marshal><string>Hello World !</string></marshal>'
  >>> file_like_object.seek(0)
  >>> xml_marshaller.load(file_like_object)
  'Hello World !'

xml_marshaller can also output xml with qualified names::


  >>> from xml_marshaller import xml_marshaller
  >>> xml_marshaller.dumps_ns('Hello World !')
  '<marshal:marshal xmlns:marshal="http://www.erp5.org/namespaces/marshaller"><marshal:string>Hello World !</marshal:string></marshal:marshal>'


You can also use your own URI::

  >>> from xml_marshaller.xml_marshaller import Marshaller
  >>> marshaller = Marshaller(namespace_uri='http://my-custom-namespace-uri/namespace')
  >>> marshaller.dumps('Hello World !')
  '<marshal:marshal xmlns:marshal="http://my-custom-namespace-uri/namespace"><marshal:string>Hello World !</marshal:string></marshal:marshal>'

