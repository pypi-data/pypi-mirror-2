import isapi_wsgi
from os import path
from pprint import PrettyPrinter
import sys
from traceback import format_exc

class ErrorApp(object):
    """ this will be used if an exception is caused by the iwhelper import """
    def __init__(self, trace, debug_info):
        self.debug_info = debug_info
        self.trace = trace

    def __call__(self, environ, start_response):
        if self.debug_info:
            envstr = PrettyPrinter().pformat(environ)
            syspath = PrettyPrinter().pformat(sys.path)
            output = '<pre>== TRACE ==\n\n%s\n\n== ENVIRON ==\n\n%s\n\n== SYS.PATH ==\n\n%s</pre>' % (self.trace, envstr, syspath)
        else:
            output = """
                <h1>OOPS...ISAPIWSGIHelper caught an exception</h1>
                <p>But I can't show you details just yet.  Find the _loader.py
                file for this website and look for the line:</p>
                <pre style="font-face: mono">
except Exception, e:
    wsgiapp = ErrorApp(format_exc(), debug_info=False)
</pre>
                <ol>
                    <li>set "debug_info=<strong>True</strong>"</li>
                    <li>restart the app pool</li>
                    <li>refresh the page</li>
                    <li>When you have fixed the exception, change "debug_info=<strong>False</strong>".  Not doing
                    so leaves open the posibility of a malicious user getting information about your system.</li>
                </ol>
            """
        # leave as 200 OK otherwise IIS shows the default 500 page, not our
        # HTML
        start_response('200 OK', [('content-type', 'text/html')])
        return [output]

try:
    from iwhelper.utils import ExceptionCatcher
    from appinit import __wsgiapp__ as wsgiapp
    wsgiapp = ExceptionCatcher(path.dirname(__file__), wsgiapp)
except Exception, e:
    wsgiapp = ErrorApp(format_exc(), debug_info=False)

# The entry points for the ISAPI extension.
def __ExtensionFactory__():
    return isapi_wsgi.ISAPIThreadPoolHandler(wsgiapp)

if __name__ == '__main__':
    """
        if all troubleshooting fails, install werkzeug and run _loader.py
        with python from a cmd prompt:

        > python _loader.py

        then browser to http://localhost:8080/ and look for exceptions
        on stderr.
    """
    from werkzeug.serving import run_simple
    run_simple('localhost', 8080, wsgiapp, use_reloader=True)
