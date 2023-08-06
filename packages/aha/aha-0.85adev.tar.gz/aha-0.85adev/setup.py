"""
Aha
==================
Aha is a framework made specially for Google App Engine. Here are some quick instruction getting started with it. For more details, visit our website :-).

  http://coreblog.org/aha

Or you can get source code from the repository.

  http://code.google.com/p/aha-gae/

What is aha
-----------------------
Aha is a web application framework. It has been developed hoping it will be the best way to propagate your 'aha!' into the cloud :-).

Aha has following features.

- rails like routing
- class base controller
- mako template ( for speed ;-) )
- db / query cache
- form, field generation
- plugins
- development with buildout
- easy to make admin/crud interface
- interactive debug interface using werkzeug
- appstats integration
- decorator based authentication mechanizm
- plagable authentication mecanizm
- i18n
- DRY


Quickstart
-----------------------
To start playing with aha, download bootstrap from url bellow.

  http://aha-gae.googlecode.com/files/project.zip

After extracting the archive, move to the folder you'll get and just type

  python bootstrap.py

Next step is to launch buildout command. Make sure that you have internet connection, because it will download libraries via the internet.

  bin/buildout

Then, launch app in local development environment. All the stuff required to run application are under app directory. So you may give 'app' argument to the command.

  bin/dev_appserver app

Now it's time to visit your fiest aha application's screen :-). Type http://127.0.0.1:8080/ to see initial page of aha's default application.
"""

from setuptools import setup, find_packages
import sys, os

version = '0.85a'

setup(name='aha',
      version=version,
      description=("aha is a web application framework specialized for"
                   " Google App Engine."),
      long_description = __doc__,
      keywords= 'web appengine framework',
      author = 'Atsushi Shibata',
      author_email = 'shibata@webcore.co.jp',
      url = 'http://coreblog.org/aha',
      license = 'BSD',
      platforms = 'any',
      include_package_data = True,
      packages = [
        'aha',
        'aha.auth',
        'aha.controller',
        'aha.dispatch',
        'aha.i18n',
        'aha.model',
        'aha.modelcontroller',
        'aha.session',
        'aha.widget',
        'aha.wsgi',
      ],
      namespace_packages = [
        'aha',
        'aha.controller',
        'aha.widget',
        'aha.wsgi',
      ],
      zip_safe = True,
      install_requires = [
          # -*- Extra requirements: -*-
          'routes',
          'formencode',
          'mako',
          'baker',
          'werkzeug',
      ],
      classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
      ],
      )
