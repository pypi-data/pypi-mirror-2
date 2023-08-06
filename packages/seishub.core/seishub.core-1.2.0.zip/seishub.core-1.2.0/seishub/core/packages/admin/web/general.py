# -*- coding: utf-8 -*-
"""
General configuration panels for the web-based administration service.
"""

from seishub.core.core import Component, implements
from seishub.core.db import DEFAULT_POOL_SIZE, DEFAULT_MAX_OVERFLOW
from seishub.core.defaults import DEFAULT_COMPONENTS
from seishub.core.exceptions import SeisHubError
from seishub.core.log import LOG_LEVELS, ERROR
from seishub.core.packages.interfaces import IAdminPanel
from seishub.core.util.text import getFirstSentence
from sqlalchemy import create_engine
from twisted.application import service
from twisted.internet import reactor
import inspect
import os
import sys


class BasicPanel(Component):
    """
    Basic configuration.
    """
    implements(IAdminPanel)

    template = 'templates' + os.sep + 'general_basic.tmpl'
    panel_ids = ('admin', 'General', 'basic', 'Basic Settings')
    has_roles = ['SEISHUB_ADMIN']

    def render(self, request):
        data = {
            'log_levels': dict([(v, k) for k, v in LOG_LEVELS.iteritems()]),
            'themes': self.root.themes
        }
        if request.method == 'POST':
            host = request.args0.get('host', 'localhost')
            description = request.args0.get('description', '')
            google_api_key = request.args0.get('google_api_key', 'localhost')
            log_level = request.args0.get('log_level', 'ERROR').upper()
            clearlogs = request.args0.get('clear_logs_on_startup', False)
            theme = request.args0.get('theme', 'magic')
            self.config.set('seishub', 'host', host)
            self.config.set('seishub', 'description', description)
            self.config.set('seishub', 'log_level', log_level)
            self.config.set('seishub', 'clear_logs_on_startup', clearlogs)
            self.config.set('web', 'admin_theme', theme)
            self.config.set('web', 'google_api_key', google_api_key)
            self.config.save()
            self.env.xslt_params['google_api_key'] = google_api_key
            if self.env.log.log_level != LOG_LEVELS.get(log_level, ERROR):
                self.env.log.log("Setting log level to %s" % log_level)
                self.env.log.log_level = LOG_LEVELS.get(log_level, ERROR)
            data['info'] = "Options have been saved."
        data.update({
          'instance': self.config.path,
          'host': self.config.get('seishub', 'host'),
          'description': self.config.get('seishub', 'description'),
          'theme': self.config.get('web', 'admin_theme'),
          'google_api_key': self.config.get('web', 'google_api_key'),
          'log_level': self.config.get('seishub', 'log_level'),
          'clear_logs_on_startup':
                self.config.getbool('seishub', 'clear_logs_on_startup')
        })
        return data


class DatabasePanel(Component):
    """
    Database configuration.
    """
    implements(IAdminPanel)

    template = 'templates' + os.sep + 'general_database.tmpl'
    panel_ids = ('admin', 'General', 'database', 'Database')
    has_roles = ['SEISHUB_ADMIN']

    def render(self, request):
        db = self.db
        data = {
          'db': db,
          'uri': self.config.get('db', 'uri'),
          'pool_size': self.config.getint('db', 'pool_size'),
          'max_overflow': self.config.getint('db', 'max_overflow'),
        }
        if db.engine.name == 'sqlite':
            data['info'] = ("SQLite Database enabled!", "A SQLite database "
                            "should never be used in a productive "
                            "environment!<br />Instead try to use any "
                            "supported database listed at "
                            "<a href='http://www.sqlalchemy.org/trac/wiki/"
                            "DatabaseNotes'>http://www.sqlalchemy.org/trac/"
                            "wiki/DatabaseNotes</a>.")
        if request.method == 'POST':
            uri = request.args0.get('uri', '')
            pool_size = request.args0.get('pool_size' , DEFAULT_POOL_SIZE)
            max_overflow = request.args0.get('max_overflow',
                                             DEFAULT_MAX_OVERFLOW)
            verbose = request.args0.get('verbose', False)
            self.config.set('db', 'verbose', verbose)
            self.config.set('db', 'pool_size', pool_size)
            self.config.set('db', 'max_overflow', max_overflow)
            data['uri'] = uri
            try:
                engine = create_engine(uri)
                engine.connect()
            except:
                data['error'] = ("Could not connect to database %s" % uri,
                                 "Please make sure the database URI has " + \
                                 "the correct syntax: dialect://user:" + \
                                 "password@host:port/dbname.")
            else:
                self.config.set('db', 'uri', uri)
                data['info'] = ("Connection to database was successful",
                                "You have to restart SeisHub in order to " + \
                                "see any changes at the database settings.")
            self.config.save()
        data['verbose'] = self.config.getbool('db', 'verbose')
        data['pool_size'] = self.config.getint('db', 'pool_size')
        data['max_overflow'] = self.config.getint('db', 'max_overflow')
        return data


class ConfigPanel(Component):
    """
    General configuration.
    """
    implements(IAdminPanel)

    template = 'templates' + os.sep + 'general_config.tmpl'
    panel_ids = ('admin', 'General', 'ini', 'seishub.ini')
    has_roles = ['SEISHUB_ADMIN']

    def render(self, request):
        data = {}
        sections = self.config.sections()
        data['sections'] = sections
        data['options'] = {}
        for s in sections:
            options = self.config.options(s)
            data['options'][s] = options
        return data


class LogsPanel(Component):
    """
    Web based log file viewer.
    """
    implements(IAdminPanel)

    template = 'templates' + os.sep + 'general_logs.tmpl'
    panel_ids = ('admin', 'General', 'logs', 'Logs')
    has_roles = ['SEISHUB_ADMIN']

    def render(self, request):
        log_file = os.path.join(self.env.getInstancePath(), 'logs',
                                'seishub.log')
        try:
            fh = open(log_file, 'r')
            logs = fh.readlines()
            fh.close()
        except:
            logs = ["Can't open log file."]
        error_logs = logs[-500:]
        data = {
          'errorlog': error_logs,
        }
        return data


class UsersPanel(Component):
    """
    Administration of users.
    """
    implements(IAdminPanel)

    template = 'templates' + os.sep + 'general_users.tmpl'
    panel_ids = ('admin', 'General', 'permission-users', 'Users')
    has_roles = ['SEISHUB_ADMIN']

    def render(self, request):
        data = {}
        # process POST request
        if request.method == 'POST':
            args = request.args
            if 'add-user' in args.keys():
                data['action'] = 'add'
            elif 'edit-user' in args.keys():
                data = self._getUser(args)
            elif 'delete' in args.keys():
                data = self._deleteUser(args)
            elif 'add' in args.keys():
                data['action'] = 'add'
                data.update(self._addUser(args))
            elif 'edit' in args.keys():
                data['action'] = 'edit'
                data.update(self._editUser(args))
        # default values
        result = {
            'id': '',
            'uid': 1000,
            'name': '',
            'email': '',
            'institution': '',
            'permissions': 755,
            'users': self.auth.users,
            'action': ''
        }
        result.update(data)
        return result

    def _getUser(self, args):
        """
        Get user data.
        """
        data = {}
        id = args.get('id', [''])[0]
        if not id:
            data['error'] = "No user selected."
        else:
            user = self.auth.getUser(id)
            data['id'] = user.id
            data['uid'] = user.uid
            data['name'] = user.name
            data['email'] = user.email
            data['institution'] = user.institution
            data['permissions'] = user.permissions
            data['action'] = 'edit'
        return data

    def _addUser(self, args):
        """
        Add a new user.
        """
        data = {}
        id = data['id'] = args.get('id', [''])[0]
        try:
            uid = data['uid'] = int(args.get('uid', [''])[0])
        except:
            uid = data['uid'] = 1000
        password = args.get('password', [''])[0]
        confirmation = args.get('confirmation', [''])[0]
        name = data['name'] = args.get('name', [''])[0]
        email = data['email'] = args.get('email', [''])[0]
        institution = data['institution'] = args.get('institution', [''])[0]
        try:
            permissions = int(args.get('permissions', [''])[0])
        except:
            permissions = 755
        if not id:
            data['error'] = "No user id given."
        elif not name:
            data['error'] = "No user name given."
        elif password != confirmation:
            data['error'] = "Password and password confirmation are not equal!"
        else:
            try:
                self.auth.addUser(id=id, name=name, password=password, uid=uid,
                                  email=email, institution=institution,
                                  permissions=permissions)
            except SeisHubError, e:
                # password checks are made in self.auth.addUser method 
                data['error'] = str(e)
            except Exception, e:
                self.log.error("Error adding new user", e)
                data['error'] = "Error adding new user", e
            else:
                data = {'info': "New user has been added."}
                data['action'] = None
        return data

    def _editUser(self, args):
        """
        Modify user information.
        """
        data = {}
        id = data['id'] = args.get('id', [''])[0]
        try:
            uid = data['uid'] = int(args.get('uid', [''])[0])
        except:
            uid = data['uid'] = 1000
        password = args.get('password', [''])[0]
        confirmation = args.get('confirmation', [''])[0]
        name = data['name'] = args.get('name', [''])[0]
        email = data['email'] = args.get('email', [''])[0]
        institution = data['institution'] = args.get('institution', [''])[0]
        try:
            permissions = int(args.get('permissions', [''])[0])
        except:
            permissions = 755
        if not id:
            data['error'] = "No user id given."
        elif not name:
            data['error'] = "No user name given."
        elif password != confirmation:
            data['error'] = "Password and password confirmation are not equal!"
        else:
            try:
                self.auth.updateUser(id=id, name=name, password=password,
                                     uid=uid, email=email,
                                     institution=institution,
                                     permissions=permissions)
            except SeisHubError, e:
                # password checks are made in self.auth.addUser method 
                data['error'] = str(e)
            except Exception, e:
                self.log.error("Error updating user", e)
                data['error'] = "Error updating user", e
            else:
                data = {'info': "User information have been updated."}
                data['action'] = None
        return data

    def _deleteUser(self, args):
        """
        Delete one or multiple users.
        """
        data = {}
        id = args.get('id', [''])[0]
        if not id:
            data['error'] = "No user selected."
        else:
            try:
                self.auth.deleteUser(id=id)
            except SeisHubError(), e:
                # checks are made in self.auth.deleteUser method 
                data['error'] = str(e)
            except Exception, e:
                self.log.error("Error deleting user", e)
                data['error'] = "Error deleting user", e
            else:
                data = {'info': "User has been deleted."}
        return data


class PluginsPanel(Component):
    """
    Administration of plug-ins.
    """
    implements(IAdminPanel)

    template = 'templates' + os.sep + 'general_plugins.tmpl'
    panel_ids = ('admin', 'General', 'plug-ins', 'Plug-ins')
    has_roles = ['SEISHUB_ADMIN']

    def render(self, request):
        error = None
        if request.method == 'POST':
            if 'update' in request.args:
                error = self._updatePlugins(request)
                if not error:
                    request.redirect(request.uri)
                    request.finish()
                    return ""
            if 'reload' in request.args:
                self._refreshPlugins()
        return self._viewPlugins(request, error)

    def _refreshPlugins(self):
        from seishub.core.util.loader import ComponentLoader
        ComponentLoader(self.env)

    def _updatePlugins(self, request):
        """
        Update components.
        """
        enabled = request.args.get('enabled', [])
        error = []

        from seishub.core.core import ComponentMeta
        for component in ComponentMeta._components:
            module = sys.modules[component.__module__]
            modulename = module.__name__
            classname = modulename + '.' + component.__name__
            if classname in enabled or classname in DEFAULT_COMPONENTS or \
                modulename in DEFAULT_COMPONENTS:
                if not self.env.isComponentEnabled(classname):
                    msg = self.env.enableComponent(component, update=False)
                    if msg and msg not in error:
                        error.append(msg)
            elif self.env.isComponentEnabled(classname):
                msg = self.env.disableComponent(component, update=False)
                if msg and msg not in error:
                    error.append(msg)
        # call update on the end
        self.env.update()
        return error

    def _viewPlugins(self, request, error=None):
        plugins = {}
        from seishub.core.core import ComponentMeta
        for component in ComponentMeta._components:
            try:
                module = sys.modules[component.__module__]
            except:
                continue
            description = getFirstSentence(inspect.getdoc(module))
            modulename = module.__name__
            classname = modulename + '.' + component.__name__
            plugin = {
              'name': component.__name__,
              'module': module.__name__,
              'file': module.__file__,
              'classname': classname,
              'description': getFirstSentence(inspect.getdoc(component)),
              'enabled': self.env.isComponentEnabled(classname),
              'required': classname in DEFAULT_COMPONENTS or \
                          modulename in DEFAULT_COMPONENTS,
            }
            plugins.setdefault(modulename, {})
            plugins[modulename].setdefault('plugins', []).append(plugin)
            plugins[modulename]['description'] = description
        data = {
          'sorted_plugins': sorted(plugins),
          'plugins': plugins,
          'error': error,
        }
        return data


class ServicesPanel(Component):
    """
    Administration of services.
    """
    implements(IAdminPanel)

    template = 'templates' + os.sep + 'general_services.tmpl'
    panel_ids = ('admin', 'General', 'services', 'Services')
    has_roles = ['SEISHUB_ADMIN']

    def render(self, request):
        if request.method == 'POST':
            if 'shutdown' in request.args:
                self._shutdownSeisHub()
            elif 'reload' in request.args:
                self._changeServices(request)
            elif 'restart' in request.args:
                self._restartSeisHub()
        data = {
          'services': service.IServiceCollection(self.env.app),
        }
        return data

    def _shutdownSeisHub(self):
        reactor.stop() #@UndefinedVariable

    def _restartSeisHub(self):
        raise NotImplemented

    def _changeServices(self, request):
        serviceList = request.args.get('service', [])
        for srv in service.IServiceCollection(self.env.app):
            if srv.running and not srv.service_id in serviceList:
                self.env.disableService(srv.service_id)
            elif not srv.running and srv.service_id in serviceList:
                self.env.enableService(srv.service_id)
