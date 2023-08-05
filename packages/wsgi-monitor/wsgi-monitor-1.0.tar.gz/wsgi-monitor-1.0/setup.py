from distutils.core import setup

setup(
    name = "wsgi-monitor",
    version = "1.0",
    description = "Auto-reload WSGI server when files change.",
    url = "http://bitbucket.org/schinckel/wsgi-monitor",
    author = "Matthew Schinckel",
    author_email = "matt@schinckel.net",
    py_modules = [
        "wsgi_monitor",
    ],
    classifiers = [
        'Programming Language :: Python',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Framework :: Django',
    ],
)
