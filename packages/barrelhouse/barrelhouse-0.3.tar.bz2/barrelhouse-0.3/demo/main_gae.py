
import os
import sys
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

demodir = os.path.abspath(os.path.dirname(__file__))
libdir = os.path.join(demodir, 'lib')
templatesdir = os.path.join(demodir, 'templates')
sys.path.insert(0, libdir)

from beaker.middleware import SessionMiddleware

import djinn

djinn.settings.TEMPLATE_DIRS = (templatesdir,)
from djinn import render_template
import barrelhouse



beaker_opts = {
      'session.type': 'ext:google',
      'session.key': 'barrelhouse.session.id',
}
beaker_environ_key = 'barrelhouse.beaker.session'


#def render_template(filename, **kw):
#    path = os.path.join(templatesdir, filename)
#    return str(render(path, kw))

class BarrelHouseBaseHandler(webapp.RequestHandler):

    def initialize(self, request, response):
        super(BarrelHouseBaseHandler, self).initialize(request, response)
        self.request.user = barrelhouse.get_current_user(request.environ)

def login_required(func):
    def inner(self, *args, **kw):
        if not self.request.user:
            self.redirect(barrelhouse.settings.SIGN_IN_URL)
        else:
            func(self, *args, **kw)
    return inner

class MainPage(BarrelHouseBaseHandler):

    def get(self):
        d = dict(
                user=self.request.user,
                SIGN_IN_URL=barrelhouse.settings.SIGN_IN_URL,
                SIGN_OUT_URL=barrelhouse.settings.SIGN_OUT_URL,
                )
        self.response.out.write(djinn.render_template('index.html', d))

class NotMainPage(BarrelHouseBaseHandler):

    @login_required
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('Hello, this is page %s\n' % self.request.url)
        self.response.out.write('You are: %s' % self.request.user)

dispatch = [
        ('/', MainPage),
        ('/.*', NotMainPage),
]

application = webapp.WSGIApplication(dispatch, debug=True)
application = barrelhouse.AuthOpenIDHandler(application)
                

def main():
    run_wsgi_app(
            SessionMiddleware(
                wrap_app=application,
                config=beaker_opts,
                environ_key=beaker_environ_key
                )
            )

if __name__ == "__main__":
    main()

