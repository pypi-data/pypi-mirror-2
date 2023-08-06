# -*- coding: utf-8 -*-
# appinits.py
# Init functions for application

__author__  = 'Atsushi Shibata <shibata@webcore.co.jp>'
__docformat__ = 'plaintext'
__licence__ = 'BSD'

__all__ = ['initConfig', 'initPlugins', 'run']

import os
import sys
import re
import logging
import wsgiref.handlers


def initConfig(basedir):
    """
    Initialize config object
    """
    # add the project's directory to the import path list.
    sys.path = [basedir,
              os.path.join(basedir, 'application'),
              os.path.join(basedir, 'lib')]+sys.path

    import aha
    config = aha.Config()

    # setup the templates location
    config.application_dir = os.path.join(basedir, 'application')
    config.messages_dir = os.path.join(config.application_dir, 'messages')
    config.template_dirs = [os.path.join(config.application_dir, 'template'),
                            'plugin']

    config.debug = False
    config.useappstatus = False
    if os.environ.get('SERVER_SOFTWARE', '').startswith('Dev'):
        config.debug = True

    return config


def initPlugins(basedir):
    """
    Initialize the installed plugins
    """
    plugin_root = os.path.join(basedir, 'plugin')
    if os.path.exists(plugin_root):
        plugins = os.listdir(plugin_root)
        for plugin in plugins:
            if not re.match('^__|^\.', plugin):
                try:
                    exec('from plugin import %s' % plugin)
                except ImportError, e:
                    from traceback import format_exc
                    logging.error('Unable to import %s' % (plugin))
                    logging.error(format_exc())
                except SyntaxError, e:
                    from traceback import format_exc
                    logging.error('Unable to import name %s' % (plugin))
                    logging.error(format_exc())


_debugged_app = None

def run(debug = False, useappstatus = False):
    """
    A function to run wsgi server
    """
    if debug:
        # use our debug.utils with Jinja2 templates
        from aha.wsgi.cwsgiapp import (CWSGIApplication, CustomHandler,
                                           MainHandler)
        from aha.wsgi.debug import utils

        app = CWSGIApplication(
                [(r'.*', MainHandler)],
                debug = debug)

        sys.modules['werkzeug.debug.utils'] = utils

        import inspect
        inspect.getsourcefile = inspect.getfile

        from werkzeug import DebuggedApplication
        global _debugged_app
        if not _debugged_app:
            _debugged_app = app = DebuggedApplication(app, evalex = True)
        else:
            app = _debugged_app

        if useappstatus:
            from google.appengine.ext.appstats import recording
            app = app = recording.appstats_wsgi_middleware(app)

            from google.appengine.ext.webapp.util import run_wsgi_app
            run_wsgi_app(app)
        else:
            CustomHandler().run(app) 

    else:
        from google.appengine.ext.webapp.util import run_wsgi_app
        from google.appengine.ext.webapp import WSGIApplication
        from aha.wsgi.cwsgiapp import MainHandler
        app = WSGIApplication(
                [(r'.*', MainHandler)],
                debug = debug)
        if useappstatus:
            from google.appengine.ext.appstats import recording
            app = app = recording.appstats_wsgi_middleware(app)

        run_wsgi_app(app)
