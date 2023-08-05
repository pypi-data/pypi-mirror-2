from setuptools import setup, find_packages

"""
Sanity
------

A quick and simple task manager built for teams in an intranet setting.
It's very simple to use by just about anyone on a team.

**Note**: This is in early stages of development, and may not be particularly
useful to many people.

Quickstart
``````````
Assuming you're using a WSGI-compatible web server (for instance, the
`mod_wsgi <http://code.google.com/p/modwsgi/>`_ module for Apache or
`gunicorn <http://gunicorn.org/>`_ with other web servers), you can simply put
the following into a file called *sanity.wsgi* and point your web server to
it:

::

    from sanity import app

More example scripts are available in the /contrib/ directory.


Links
`````

* `website <http://bitbucket.org/aaront/sanity/>`_
* `documentation <http://flask.pocoo.org/docs/>`_

"""

setup(
    name='Sanity',
    version='0.2.5',
    url='http://bitbucket.org/aaront/sanity/',
    license='Apache 2.0',
    author='Aaron Toth',
    author_email='atoth89@gmail.com',
    description='A team-based task manager intranet application',
    long_description=open('README.txt').read(),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask>=0.4',
        'Flask-SQLAlchemy'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
    ]
)
