
import os

from openid.store.filestore import FileOpenIDStore
from template import render

workingdir = os.path.abspath(os.path.dirname(__file__))
templatesdir = os.path.join(workingdir, 'templates')

def render_template(filename, **kw):
    path = os.path.join(templatesdir, filename)
    return str(render(path, kw))

barrelhouse_SESSION_USER_KEY = 'barrelhouse.demo.user'

def barrelhouse_get_store():
    return FileOpenIDStore("_oid")

def barrelhouse_get_session(environ):
    return environ['paste.session.factory']()

def barrelhouse_render_signin(context):
    return render_template('signin.html', **context.todict())

def barrelhouse_on_openid_success(info, context):
    session = context.environ['paste.session.factory']()
    session[barrelhouse_SESSION_USER_KEY] = info['claimed_id']
