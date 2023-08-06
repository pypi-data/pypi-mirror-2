Flask-Enterprise
================

.. module:: flaskext.enterprise

Flask-Enterprise brings enterprise level capabilities to your Flask
application.  It aims for the professional user and interoperability with
multi-tier applications both internally and over the network.

It's available under the OSI approved `CDDL`_ license.  It's developed and
maintained by `Massive of Rock Inc <http://massive.immersedcode.org/>`_.
The package is in-house developed and the source tree is privately held.
We currently do not accept patches due to legal reasons but you are free
to modify the code as necessary for as long as you are in compliance with
the CDDL.

Latest version is Flask-Enterprise 1.0, released on April 1st 2011.

.. _CDDL: http://www.opensource.org/licenses/cddl1

Features
--------

-   Support for the industry standard enterprise protocols SOAP, WSDL and
    XML-RPC
-   Secure: code base is audited regularly and carefully
-   Strong foundation: the enterprise extension is based on powerful base
    libraries widely deployed in business applications.
-   Backwards compatible: we guarantee 100% backwards compatibility

Installation
------------

Flask-Enterprise is available from the Python Enterprise Package Index
(`PyPI`_) but depends on a wider range of core libraries so it's
encouraged to install it with the Python Installation Program (`pip`_)::

    pip install Flask-Enterprise

.. _PyPI: http://pypi.python.org/
.. _pip: http://pypi.python.org/pypi/pip

Creating SOAP Services
----------------------

This example shows how you can easily create a SOAP service with
Flask-Enterprise.  We will implement one service with one method that is
exposed over SOAP/WSDL::

    from time import ctime
    from flask import Flask
    from flaskext.enterprise import Enterprise

    app = Flask(__name__)
    enterprise = Enterprise(app)

    class DemoService(enterprise.SOAPService):

        @enterprise.soap(_returns=enterprise._sp.String)
        def get_time(self):
            return ctime()

By default the soap service will be available at ``/_enterprise/soap`` but
this endpoint can be overriden by setting the
:attr:`~EnterpriseSOAPService.__soap_server_address__` attribute.  If you
append ``?wsdl`` to the URL it will serve a WSDL document.  Multiple
services can be registered to the application, however in that case the
server address has to be explicitly set (ie: ``/_enterprise/soap2``).

Interfacing SOAP/WSDL Services
------------------------------

In order to speak to WSDL services you can use the
:meth:`Enterprise.connect_to_soap_service` function.  It will return a new
client that can be used to connect to a remote service::


    client = enterprise.connect_to_soap_service('http://example.com/?wsdl')

    @app.route('/time')
    def index():
        time = client.service.get_time()
        ...

Creating XMLRPC Services
------------------------

XMLRPC Services work similar to SOAP services, but have a simpler API due
to the missing envelopes::

    from time import ctime
    from flask import Flask
    from flaskext.enterprise import Enterprise

    app = Flask(__name__)
    enterprise = Enterprise(app)

    class DemoService(enterprise.XMLRPCService):

        @enterprise.xmlrpc('getTime')
        def get_time(self):
            return ctime()

The service will by default be available at ``/_enterprise/xmlrpc`` but
this can be changed by setting the
:attr:`~EnterpriseXMLRPCService.__xmlrpc_server_address__` attribute.
Multiple services can be registered to the application, however in that
case the server address has to be explicitly set (ie:
``/_enterprise/xmlrpc2``).

Interfacing XMLRPC Services
---------------------------

In order to speak to WSDL services you can use the
:meth:`Enterprise.connect_to_xmlrpc_service` function.  It will return a new
client that can be used to connect to a remote service::


    client = enterprise.connect_to_xmlrpc_service('http://example.com/foo')

    @app.route('/time')
    def index():
        time = client.getTime()
        ...

API
---

.. class:: Enterprise

   This class acts as the central manager.  When it's created it is
   automatically registered with the application.  The application and the
   manager are connected by the :class:`EnterpriseController`.

   The enterprise manager also automatically handles service registration
   for you.  Instead of subclassing from :class:`EnterpriseXMLRPCService`
   and :class:`EnterpriseXMLRPCService` subclass
   ``enterprise.XMLRPCService`` and ``enterprise.SOAPService`` to take
   advantage of automatic service registrations.

   .. method:: soap([signature[, returns=ReturnType]])

      A decorator to mark a method as SOAP callable endpoint.  It takes a
      number of arguments which can be :attr:`_sp` or :attr:`_scls`
      objects and a keyword argument named `_returns` that specifies the
      return type.

      Example::

        @soap(String,Integer,_returns=Array(String))
        def say_hello(self,name,times):
            results = []
            for i in range(0, times):
                results.append('Hello, %s' % name)
            return results

      This method is to be used for exposed methods in a
      :class:`EnterpriseSOAPService` subclass.

   .. method:: xmlrpc(name)

      Marks a function as xmlrpc callable.  The name of the xmlrpc method
      has to be provided explicitly as first argument::

        @xmlpc('sayHello')
        def say_hello(self, name, times):
            results = []
            for i in range(0, times):
                results.append('Hello, %s' % name)
            return results

      This method is to be used for exposed methods in a
      :class:`EnterpriseXMLRPCService` subclass.

   .. method:: connect_to_soap_service(url)

      Returns a new connection to a remote SOAP service:

      >>> url = 'http://localhost:5000/_enterprise/soap?wsdl'
      >>> hello_client = enterprise.connect_to_soap_service(url)
      >>> result = hello_client.service.say_hello('Peter', 5)
      >>> print result
      (stringArray){
         string[] =
            "Hello, Peter",
            "Hello, Peter",
            "Hello, Peter",
            "Hello, Peter",
            "Hello, Peter"
       }

      The `service` attribute acts as a proxy to the remote service.
      
   .. method:: connect_to_xmlrpc_service(url)

      Returns a new proxy to a remote XMLRPC service:

      >>> url = 'http://localhost:5000/_enterprise/xmlrpc'
      >>> hello_client = enterprise.connect_to_xmlprc_service(url)
      >>> result = hello_client.sayHello('Peter', 3)
      [u'Hello, Peter', u'Hello, Peter', u'Hello, Peter']

   .. attribute:: _sp
   .. attribute:: _sb
   .. attribute:: _scls

      Provides access to primitive, binary and class soap modelling
      objects.  See :ref:`soap-modelling` for more information.

   .. attribute:: controller

      The associated :class:`EnterpriseController`.  Can be used to attach
      enterprise services directly if they were created by subclassing the
      core classes from :mod:`flaskext.enterprise` directly.

.. class:: EnterpriseController

   Central registration point and connection between a Flask application
   and the :class:`Enterprise` manager object.

   .. method:: register_soap_service(service)

      Registers a :class:`EnterpriseSOAPService` with the controller.

   .. method:: register_xmlrpc_service(service)

      Registers a :class:`EnterpriseXMLRPCService` with the controller.

.. class:: EnterpriseXMLRPCService

   Baseclass for enterprise XMLRPC services.

   .. attribute:: __xmlrpc_server_address__

      The address for the XMLRPC server.  Defaults to
      ``/_enterprise/xmlrpc``.

.. class:: EnterpriseSOAPService

   Baseclass for enterprise SOAP services.

   .. attribute:: __soap_server_address__

      The address for the SOAP server.  Defaults to
      ``/_enterprise/soap``.

   .. attribute:: __soap_target_namespace__

      The target namespace for the SOAP envelope.  Defaults to ``'tns'``.

.. _soap-modelling:

SOAP Models
-----------

In Flask-Enterprise, the type are the components responsible for
converting indivdual parameters to and from xml, as well as supply the
information necessary to build the wsdl. Flask-Enterprise has many built-in type
that give you most of the common datatypes generally needed.

Primitives
``````````

The basic primitive types are `String`, `Integer`,
`DateTime`, `Null`, `Float`, `Boolean`.
These are some of the most basic blocks within Flask_Enterprise:

>>> String = enterprise._sp.String
>>> from lxml import etree
>>> parent = etree.Element("parent")
>>> String.to_parent_element("abcd", "tns", parent)
>>> string_element = parent.getchildren()[0]
>>> print etree.tostring(string_element)
<ns0:retval xmlns:ns0="tns" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="xs:string">abcd</ns0:retval>
>>> print String.from_xml(string_element)
abcd
>>> String.get_type_name()
'string'
>>> String.get_type_name_ns()
'xs:string'

Arrays
``````

The lone collection type available in Flask-Enterprise is the `Array` type.
Unlike the primitive type, Arrays need to be instantiated with
the proper internal type so they can properly (de)serialize the data. Arrays
are homogeneous, meaning that the data they hold are all of the same
type. For mixed typing or more dynamic data, use the Any type.

>>> String = enterprise._sp.String
>>> Array = enterprise._scls.Array
>>> from lxml import etree
>>> parent = etree.Element("parent")
>>> array_serializer = Array(String)
>>> array_serializer.to_parent_element(['a','b','c','d'], 'tns', parent)
>>> print etree.tostring(element)
<ns0:stringArray xmlns:ns0="tns"><ns1:string xmlns:ns1="None" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="xs:string">a</ns1:string>
<ns2:string xmlns:ns2="None" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="xs:string">b</ns2:string>
<ns3:string xmlns:ns3="None" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="xs:string">c</ns3:string>
<ns4:string xmlns:ns4="None" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="xs:string">d</ns4:string></ns0:stringArray>
>>> print array_serializer.from_xml(element)
['a', 'b', 'c', 'd']

Class
`````

The `ClassSerializer` type is used to define and serialize complex,
nested structures.

>>> String = enterprise._sp.String
>>> Integer = enterprise._sp.Integer
>>> from lxml import etree
>>> class Permission(enterprise._scls.ClassSerializer):
...	    __namespace__ = "permission"
...		application = String
...		feature = String
>>>
>>> class User(enterprise._scls.ClassSerializer):
...     __namespace__ = "user"
...		userid = Integer
...		username = String
...		firstname = String
...		lastname = String
...		permissions = Array(Permission)
>>>
>>> u = User()
>>> u.username = 'bill'
>>> u.permissions = []
>>> p = Permission()
>>> p.application = 'email'
>>> p.feature = 'send'
>>> u.permissions.append(p)
>>> parent = etree.Element('parenet')
>>> User.to_parent_element(u, 'tns', parent)
>>> element = parent[0]
>>> etree.tostring(element)
'<ns0:User xmlns:ns0="tns">
<ns1:username xmlns:ns1="None" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="xs:string">bill</ns1:username>
<ns2:firstname xmlns:ns2="None" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>
<ns3:lastname xmlns:ns3="None" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>
<ns4:userid xmlns:ns4="None" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:nil="true"/>
<ns5:permissions xmlns:ns5="None"><ns5:Permission><ns5:application xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:type="xs:string">email</ns5:application>
>>> User.from_xml(element).username
'bill'
>>>

Attachment
``````````

The `Attachment` serializer is used for transmitting binary data as
base64 encoded strings. Data in Attachment objects can be loaded manually,
or read from file.  All encoding of the binary data is done just prior to the
data being sent, and decoding immediately upon receipt of the Attachment.

>>> Attachment = enterprise._sb.Attachment
>>> from lxml import etree
>>> a = Attachment(data='my binary data')
>>> parent = etree.Element('parent')
>>> Attachment.to_parent_element(a)
>>> element = parent[0]
>>> print etree.tostring(element)
<ns0:retval xmlns:ns0="tns">bXkgYmluYXJ5IGRhdGE=
</ns0:retval>
>>> print Attachment.from_xml(element).data
my binary data
>>> a2 = Attachment(fileName='test.data') # load from file

Any
```

The `Any` type is a serializer used to transmit unstructured XML data.
Any types are very useful for handling dynamic data, and provide a very
Pythonic way for passing data using Flask-Enterprise. The Any serializer
does not perform any useful task because the data passed in and returned
are Element objects. The Any type's main purpose is to declare its
presence in the WSDL.

AnyAsDict
`````````

The `AnyAsDict` type does the same thing as the `Any` type, except it
serializes to/from dicts with lists instead of raw `lxml.etree._Element`
objects.
