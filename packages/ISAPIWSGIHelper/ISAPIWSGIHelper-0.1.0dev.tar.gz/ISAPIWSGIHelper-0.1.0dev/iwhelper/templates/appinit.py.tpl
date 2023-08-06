# This setup assumes you have the isapi-wsgi directory installed
# in the root directory of a virtualenv:
#
#  ..\myproj-venv
#     - isapi-wsgi
#     - Lib
#     - Scripts
#
# If you have isapi-wsgi installed in a different location or are not using
# a virtualenv, you CAN SAFELY DELETE THE FOLLOWING FOUR LINES.
from os import path
from iwhelper.utils import prependsitedir
spdir = path.join(path.dirname(__file__), '..', 'Lib', 'site-packages')
prependsitedir(spdir)

# replace these two lines with the necessary imports to instantiate your
# WSGI application and assign said application to __wsgiapp__.
from iwhelper.utils import hwapp
__wsgiapp__ = hwapp
