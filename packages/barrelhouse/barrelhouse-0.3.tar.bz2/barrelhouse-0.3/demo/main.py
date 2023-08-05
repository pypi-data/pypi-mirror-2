
import os
import sys

workingdir = os.path.abspath(os.path.dirname(__file__))
libdir = os.path.join(workingdir, 'lib')
barrelhousedir = os.path.abspath(os.path.join(workingdir, '..'))
templatesdir = os.path.join(workingdir, 'templates')
sys.path.insert(0, libdir)
sys.path.insert(0, barrelhousedir)
#sys.path.insert(0, '.')

from paste.session import SessionMiddleware
from template import render
import lib_config
import barrelhouse

registry = lib_config.LibConfigRegistry('config')
barrelhouse.configure(registry)

asset_types = {
        '.js': 'text/plain',
        '.css': 'text/css',
        '.png': 'image/png',
}

def render_template(filename, **kw):
    path = os.path.join(templatesdir, filename)
    return str(render(path, kw))

def demo(environ, start_response):
    request_path = environ['PATH_INFO']
    syspath = os.path.join(workingdir, request_path[1:])
    _, ext = os.path.splitext(request_path)
    asset_type = asset_types.get(ext, None)
    if asset_type:
        fobj = open(syspath)
        s = fobj.read()
        fobj.close()
        start_response('200 OK', [('Content-Type', asset_type)])
        return [s]
    user = barrelhouse.get_current_user(environ)
    if request_path == '/':
        start_response('200 OK', [('Content-Type', 'text/html')])
        s = render_template('index.html', user=user)
        return [s]
    if user is None and request_path != '/':
        continue_url = request_path
        redirect_to = '/accounts/signin?continue=' + continue_url
        start_response('302 Found', [('location', redirect_to)])
        return []
    start_response('401 Not Found', [('Content-Type', 'text/html')])
    return ['Not Found']

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    app = SessionMiddleware(barrelhouse.AuthOpenIDHandler(demo))
    srv = make_server('localhost', 8080, app)
    srv.serve_forever()

