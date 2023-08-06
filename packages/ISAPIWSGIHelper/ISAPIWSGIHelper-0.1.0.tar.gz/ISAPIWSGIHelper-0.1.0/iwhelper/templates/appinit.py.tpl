# This setup assumes you have the isapi-wsgi directory installed
# in the root directory of a virtualenv:
#
#  ..\myproj-venv
#     - isapi-wsgi
#     - Lib
#     - Scripts
#
# If you have isapi-wsgi installed in a different location or are not using
# a virtualenv, you CAN SAFELY MODIFY OR DELETE THE FOLLOWING TWO LINES.
from iwhelper.utils import prepend_site_dir
prepend_site_dir(__file__, '..', 'Lib', 'site-packages')

# replace these two lines with the necessary imports to instantiate your
# WSGI application and assign said application to __wsgiapp__.
from iwhelper.utils import hwapp
__wsgiapp__ = hwapp
