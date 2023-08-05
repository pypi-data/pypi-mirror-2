from setuptools import setup, find_packages
import sys, os

version = '0.9.2'

setup(name='xml_marshaller',
      version=version,
      description="Converting Python objects to XML and back again.",
      long_description="""
Marshals simple Python data types into a custom XML format.
The Marshaller and Unmarshaller classes can be subclassed in order
to implement marshalling into a different XML DTD.
Original Authors are XML-SIG (xml-sig@python.org).
Fully compatible with PyXML implementation, enable namespace support for
XML Input/Output.
Implemented with lxml""",
classifiers=['Development Status :: 4 - Beta',
             'Intended Audience :: Developers',
             'License :: OSI Approved :: Python License (CNRI Python License)',
             'Operating System :: OS Independent',
             'Topic :: Text Processing :: Markup :: XML'], 
      keywords='XML marshaller',
      author='XML-SIG',
      author_email='xml-sig@python.org',
      maintainer='Nicolas Delaby',
      maintainer_email='nicolas@nexedi.com',
      url='http://www.python.org/community/sigs/current/xml-sig/',
      license='Python License (CNRI Python License)',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=['lxml',],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
