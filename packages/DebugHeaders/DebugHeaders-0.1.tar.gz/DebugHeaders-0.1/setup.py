from setuptools import setup, find_packages

version = '0.1'

setup(name='DebugHeaders',
      version=version,
      description="Debug headers (and bodies) of WSGI requests and responses",
      long_description="""\
This WSGI middleware will display the headers of the incoming request
and the outgoing response.  You can also optionally display the
request or response body.

Use it like this::

    from debugheaders import DebugHeaders

    def application(environ, start_response):
        blah blah blah

    application = DebugHeaders(application,
                               show_body=True, show_response_body=True,
                               output='wsgi.errors')

`show_body` shows the request body, `show_response_body` does what you
would expect, and this information is written to the stream given by
`output` (defaults to stdout, can be any object with a ``.write()``
method, and `'wsgi.errors'` is special and means to write to
``environ['wsgi.errors']``).
""",
      classifiers=[
          "Development Status :: 4 - Beta",
          "Environment :: Web Environment",
          "Framework :: Paste",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Topic :: Internet :: WWW/HTTP :: WSGI",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware",
          ],
      keywords='wsgi debugging',
      author='Ian Bicking',
      author_email='ianb@colorstudy.com',
      #url='http://pythonpaste.org/debugheaders/',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      install_requires=[
          "Paste",
      ],
      entry_points="""
      [paste.filter_app_factory]
      main = debugheaders:make_debug_headers
      """,
      )
