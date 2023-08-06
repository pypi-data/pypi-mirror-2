import cgi
import logging

from webob import exc
from paste import fileapp

from .core import widget_context
from .resource import ResourceManager
from .render import TemplateEngine

log = logging.getLogger(__name__)

class WidgetMiddleware(object):

    def __init__(self, app,
                 compress=False,
                 script_name='/_ew_resources/',
                 url_base=None,
                 cache_max_age=60*60*24*365,
                 register_resources=True,
                 use_jsmin=False,
                 use_cssmin=False,
                 **extra_config):
        self.app = app
        self.script_name = script_name
        self.script_name_slim_js = script_name + '_slim/js'
        self.script_name_slim_css = script_name + '_slim/css'
        self.compress = compress
        if url_base is None:
            url_base = self.script_name
        self.url_base = url_base
        self.cache_max_age = cache_max_age
        self.register_resources = register_resources
        self.use_jsmin = use_jsmin
        self.use_cssmin = use_cssmin
        self._resource_manager = ResourceManager(
            compress=self.compress,
            script_name=self.script_name,
            url_base=self.url_base,
            cache_max_age=self.cache_max_age,
            use_jsmin=self.use_jsmin,
            use_cssmin=self.use_cssmin,
            )
        widget_context._resource_manager = self._resource_manager
        if self.register_resources:
            ResourceManager.register_all_resources()
        TemplateEngine.initialize(extra_config)

    def __call__(self, environ, start_response):
        widget_context.set_up(environ)
        widget_context.scheme = environ['wsgi.url_scheme']
        mgr = self._resource_manager
        if not environ['PATH_INFO'].startswith(self.script_name):
            result = self.app(environ, start_response)
        elif environ['PATH_INFO'].startswith(self.script_name_slim_js):
            result = self.serve_slim_js(
                mgr, cgi.parse_qs(environ['QUERY_STRING']).get('href', [''])[0],
                environ, start_response)
        elif environ['PATH_INFO'].startswith(self.script_name_slim_css):
            result = self.serve_slim_css(
                mgr, cgi.parse_qs(environ['QUERY_STRING']).get('href', [''])[0],
                environ, start_response)
        else:
            result = self.serve_resource(mgr, environ['PATH_INFO'][len(self.script_name):], environ, start_response)
        widget_context.tear_down()
        return result

    def serve_resource(self, mgr, res_path, environ, start_response):
        fs_path = mgr.get_filename(res_path)
        if fs_path is None:
            log.warning('Could not map %s', res_path)
            log.info('Mapped directories: %r', mgr.paths)
            return exc.HTTPNotFound(res_path)(environ, start_response)
        app = fileapp.FileApp(fs_path)
        app.cache_control(public=True, max_age=mgr.cache_max_age)
        try:
            return app(environ, start_response)
        except OSError:
            return exc.HTTPNotFound(res_path)(environ, start_response)

    def serve_slim_js(self, mgr, res_path, environ, start_response):
        data = mgr.serve_slim('js', res_path)
        app = fileapp.DataApp(data, [('Content-Type', 'text/javascript')])
        app.cache_control(public=True, max_age=mgr.cache_max_age)
        return app(environ, start_response)
            
    def serve_slim_css(self, mgr, res_path, environ, start_response):
        data = mgr.serve_slim('css', res_path)
        app = fileapp.DataApp(data, [('Content-Type', 'text/css')])
        app.cache_control(public=True, max_age=mgr.cache_max_age)
        return app(environ, start_response)

