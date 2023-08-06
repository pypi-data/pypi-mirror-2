========================
TracGoogleAppsAuthPlugin
========================

Plugin for Trac which redirects all unauthenticated requests to the login page.
This lets you easily disallow anonymous access, without the messy juggling of
permissions from the `anonymous` to `authenticated` groups and without the
confusing "permission denied" error page.

Please note that this software is currently in "alpha" state and under active
development! It has the potential to clash with other plugins; your testing
feedback is appreciated! Does it work with HTTP auth? Beats me, I use the
AccountManagerPlugin with cookie-based web login.

See: https://code.google.com/p/tracloginrequiredplugin/

Author: David A. Riggs <david.riggs@createtank.com>


License
=======

Copyright 2010 createTank, LLC

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
Version 2 as published by the Free Software Foundation.

http://www.gnu.org/licenses/old-licenses/gpl-2.0.html


Installation
============

To magically install from the PyPI,

``$> sudo easy_install TracLoginRequiredPlugin``

... or from source,

``$> sudo python setup.py install``
