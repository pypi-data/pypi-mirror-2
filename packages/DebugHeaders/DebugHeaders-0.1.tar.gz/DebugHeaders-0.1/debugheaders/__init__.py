"""
WSGI proxy application that applies a deliverance theme while
passing the request to another HTTP server
"""

from cStringIO import StringIO
import sys
from paste.request import construct_url

class DebugHeaders(object):

    """Middleware that shows all headers.
    """

    translate_keys = {
        'CONTENT_LENGTH': 'HTTP_CONTENT_LENGTH',
        'CONTENT_TYPE': 'HTTP_CONTENT_TYPE',
        }

    def __init__(self, app, show_body=False, show_response_body=False,
                 output=sys.stdout):
        self.app = app
        self.show_body = show_body
        self.show_response_body = show_response_body
        self.output = output or sys.stdout

    def __call__(self, environ, start_response):
        output = self.output
        if output == 'wsgi.errors':
            output = environ['wsgi.errors']
        output.write(
            'Incoming headers: (%s %s SCRIPT_NAME=%r)\n' %
            (environ['REQUEST_METHOD'], construct_url(environ), environ.get('SCRIPT_NAME')))
        for name, value in sorted(environ.items()):
            name = self.translate_keys.get(name, name)
            if not name.startswith('HTTP_'):
                continue
            name = name[5:].replace('_', '-').title()
            output.write('  %s: %s\n' % (name, value))
        if self.show_body:
            self.show_request_body(environ, output)

        def repl_start_response(status, headers, exc_info=None):
            output.write('Outgoing headers: (%s)\n' % status)
            for name, value in headers:
                output.write('  %s: %s\n' % (name.title(), value))
            return start_response(status, headers, exc_info)
        if self.show_response_body:
            out = []

            def capture_start_response(status, headers, exc_info=None):
                repl_start_response(status, headers, exc_info)
                return out.append
            for chunk in self.app(environ, capture_start_response):
                out.append(chunk)
            output.write('\nResponse body:\n')
            self.show_output(''.join(out), output)
            return out
        else:
            return self.app(environ, repl_start_response)

    def show_request_body(self, environ, output):
        length = int(environ.get('CONTENT_LENGTH') or '0')
        body = environ['wsgi.input'].read(length)
        environ['wsgi.input'] = StringIO(body)
        self.show_output(body, output)

    def show_output(self, data, output):
        if data:
            for line in data.splitlines():
                # This way we won't print out control characters:
                output.write(line.encode('string_escape')+'\n')
            output.write('-'*70+'\n')


def make_debug_headers(app, global_conf, show_body=False,
                       stderr=False):
    """
    Show all the headers that come to the application.

    These are printed to sys.stdout, or sys.stderr if stderr=True.  If
    show_body is true, then the body of all requests is also
    displayed.
    """
    from paste.deploy.converters import asbool
    if asbool(stderr):
        output = sys.stderr
    else:
        output = sys.stdout
    return DebugHeaders(app, show_body=asbool(show_body),
                        output=output)
