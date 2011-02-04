==========
OpenHRIWeb
==========

OpenHRIWeb is a collection of components which provides web functionalities
to the RT-Middleware system.

Requirements
------------

OpenHRIWeb requires pyxmpp, lxml and simplejson library.

pyxmpp
  http://pyxmpp.jajcus.net/

lxml
  http://codespeak.net/lxml/

simplejson
  http://pypi.python.org/pypi/simplejson/

If you are using ubuntu, required libraries will be installed by entering
following command:

 ::
 
 $ sudo apt-get install python-pyxmpp python-lxml python-simplejson


Installation
------------

There are several methods of installation available:

1. Install ubuntu package (recommended):

 a. Register OpenHRI private package archive:

    ::
    
    $ sudo apt-add-repository ppa:openhri/ppa

 b. Install OpenHRIWeb package:

    ::
    
    $ sudo apt-get update
    $ sudo apt-get install openhriweb

2. Clone the source from the repository and install:

 a. Clone from the repository:

    ::
    
    $ git clone git://github.com/yosuke/openhriweb.git openhriweb

 b. Run setup.py:

    ::
    
    $ cd openhriweb
    $ sudo python setup.py install

Components
----------

JabberRTC
  Jabber messaging component.

WebServerRTC
  Web server component.

XMLtoJSONRTC
  XML to JSON conversion component.

see https://github.com/yosuke/OpenHRIWeb/tree/master/doc for description of each components.

Changelog
---------

openhriweb-1.0

- First version.
