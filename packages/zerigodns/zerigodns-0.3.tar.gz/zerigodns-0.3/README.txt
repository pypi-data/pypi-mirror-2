Zerigo DNS - REST API - Python Module
===================================

The API documentation itself is not provided here. The latest version can
be found online at http://www.zerigo.com/docs/managed-dns/api_11.


Requirements
------------
The following are required to use this library:

- A functioning Python 2.3+ environment with HTTP (or HTTPS) access to the internet.
- Some working knowledge of the Python language.
- A Zerigo DNS account with Dynamic Updates / API Access enabled. (Visit
  https://ns.zerigo.com/ and go to Preferences to enable access.)
- The Dynamic Update / API key. (Also available on the Preferences page.)


Use
---

Basic Install:

  $ python setup.py build
  $ sudo python setup.py install

Alternative Install (Manually):

Place zerigodns directory in your Python path. Either in your Python 
installs site-packages directory or set your $PYTHONPATH environment 
variable to include a directory where the zerigodns directory lives.

Both the library (zerigodns) and example usage code (example.py) are 
heavily commented. They should serve as sufficient reference for this code.


Updates
-------
Visit http://www.bitbucket.org/petersanchez/zerigodns for updates, new versions, and 
more.


Support
-------

Python Module:

For issues with the Python API module, please use the public issue tracker at the 
repositories website: http://bitbucket.org/petersanchez/zerigodns/

Zerigo Support:

Support is generally available via standard Zerigo support options. See
http://www.zerigo.com/support for more information. Please note that support
may be limited based on your choice of Zerigo DNS services.


Comments / Suggestions
----------------------
We always welcome comments, suggestions, and constructive complaints. You can
find several ways to contact me at http://www.petersanchez.com/contact/


Copyright & Warranty
--------------------
All documentation, libraries, and sample code are 
Copyright 2009 Peter Sanchez <petersanchez@gmail.com>. The library and 
sample code are made available to you under the terms of the BSD license 
which is contained in the included file, BSD-LICENSE.

The terms here grant you no rights in regard to the Zerigo services. Please
reference Zerigo's Terms of Service for all legal information regarding
Zerigo's services.
