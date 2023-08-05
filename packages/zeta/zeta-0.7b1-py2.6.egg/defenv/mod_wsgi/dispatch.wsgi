# This file is subject to the terms and conditions defined in
# file 'LICENSE', which is part of this source code package.
#       Copyright (c) 2009 SKR Farms (P) LTD.

"""
The following files will be copied to environment directory, while 
`paster setup-app` is executed.
    defenv/mod_wsgi/dispatch.py
    defenv/mod_wsgi/__init__.py
The web master should modify the following lines in this file, to suite the
deployed zeta version and its environment.
"""


# Add the virtual Python environment site-packages directory to the path
#add-virtualenv-packages

# Avoid ``[Errno 13] Permission denied: '/var/www/.python-eggs'`` messages
import os
#add-eggcache-here

# Load the Pylons application
from paste.deploy import loadapp
#add-config-here
