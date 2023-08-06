MsJSON Mapfile serialiser
=========================

A package for converting UMN Mapserver mapscript objects to and
from JSON.

`mapscript <http://mapserver.org/mapscript/>`_

`JSON <http://www.json.org/>`_


The MsJSON package is released under the terms of the GNU LPGL Version 3
(see ``COPYRIGHT``).


Installation
------------

The MsJSON package requires a working mapscript Python library. For  
processing with json.load(s) or json.dump(s) the Python JSON module is
necessary but not required.

JSON is battery included since Python 2.6, for Python 2.5 the SimpleJSON
module can be used. It is available in the Python package index.

As soon as the package is availabe in the Python package index you can do::
    
    easy_install msjson

Meanwhile you can download a source distribution archive from
`Bitbucket <https://bitbucket.org/frankbroniewski/msjson/src>`_
available in the dist folder and then::

    python setup.py install

Development
-----------

Development is managed through bitbucket. The bitbucket archive is located
under https://bitbucket.org/frankbroniewski/msjson/src.

You are welcome to clone the project :-)::

    $ hg clone https://bitbucket.org/frankbroniewski/msjson

