# barrelhouse
# -----------
#
# WSGI-compliant OpenID authentication
#
# (c) 2010 Walter Wefft
# Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php
#
# Code is heavily based or directly extracted from two projects:
#
# Paste
# -----
# (c) 2005 Ian Bicking and contributors; written for Paste (http://pythonpaste.org)
# Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php
#
# aeoid (http://github.com/Arachnid/aeoid)
# ----------------------------------------
# AUTHOR: Nick Johnson
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

__version__ = '0.3'

import sys
import cgi
import urlparse
import urllib
import re
import types

from paste.request import construct_url, parse_formvars, parse_querystring
from openid.consumer.consumer import Consumer
from openid.association import Association as OpenIDAssociation
from openid.store import interface
from openid.store import nonce
from openid.oidutil import appendArgs
from openid.extensions import sreg
from openid.extensions import ax

from barrelhouse.conf import settings


# default implementation - override in user settings
def get_current_user(environ):
    session = settings.get_session(environ)
    return session.get(settings.SESSION_USER_KEY, None)

# default implementation - override in user settings
def set_current_user(username, environ):
    session = settings.get_session(environ)
    session[settings.SESSION_USER_KEY] = username
    if hasattr(session, 'save'):
        session.save()

# default implementation - override in user settings
def sign_out_current_user(environ):
    session = settings.get_session(environ)
    del session[settings.SESSION_USER_KEY]
    if hasattr(session, 'save'):
        session.save()

def render_signin(context, **kw):
    context.update(kw)
    context.setdefault('error', False)
    context.setdefault('status', '200 OK')
    response_headers = [('Content-type', 'text/html')]
    context.start_response(str(context.status), response_headers)
    return [settings.render_signin(context)]

def host_url(environ):
    return construct_url(
            environ,
            script_name="/",
            with_path_info=False,
            )[:-1]

def construct_return_to_url(context):
    script_name = "%s/%s" % (settings.SIGN_IN_URL, "oid_complete")
    qs = "continue=" + context.GET.get('continue', '/')
    return construct_url(
            context.environ,
            script_name=script_name,
            with_path_info=False,
            querystring=qs
            )

###########  OPENID ###############
def get_oid_consumer(environ):
    store = settings.get_store()
    session = settings.get_session(environ)
    cls = settings.consumer_class
    if isinstance(cls, basestring):
        module, cls = cls.rsplit('.', 1)
        m = __import__(module)
        cls = getattr(m, cls)
    return Consumer(session, store, cls)

def initiate_openid_login(openid_url, context):
    # Here we find out the identity server that will verify the
    # user's identity, and get a token that allows us to
    # communicate securely with the identity server.
    consumer = get_oid_consumer(context.environ)
    request = consumer.begin(openid_url)
    return_to = construct_return_to_url(context)
    realm = host_url(context.environ)
    return request.redirectURL(realm, return_to)

def complete_openid_login(context):
    consumer = get_oid_consumer(context.environ)
    return_to = construct_return_to_url(context)
    response = consumer.complete(context.GET, return_to)
    if response.status == 'success':
        return response
    elif response.status == 'cancel':
        raise BarrelHouseFailedVerificationError("Verification Cancelled")
    else:
        if hasattr(response, 'error'):
            err = response.error
        else:
            err = "OpenID Failure"
        raise BarrelHouseFailedVerificationError(err)

def get_info_from_openid_response(response):
    # adapted from aeoid
    info = Dict(
            claimed_id=response.endpoint.claimed_id,
            server_url=response.endpoint.server_url,
            )
    info.sreg = info.ax = None
    # get sreg data if available
    id_res_data = sreg.SRegResponse.fromSuccessResponse(response)
    if id_res_data is not None:
        id_res_data = dict(id_res_data)
        info.sreg = id_res_data
    
    # otherwise get ax data if available
    else:
        id_res_data = {}
        try:
            ax_data = ax.FetchResponse.fromSuccessResponse(response)
            for attruri in settings.OPENID_AX_ATTRS:
                try:
                    attrvalue = ax_data.get(attruri)
                    id_res_data[ settings.OPENID_AX_ATTRS[attruri] ] = attrvalue.pop(0)
                except (AttributeError,IndexError,KeyError):
                    pass
            # try to ensure we have a nickname (even if we fall back to email)
            if not id_res_data.has_key('nickname'):
                if id_res_data.has_key('firstname') or id_res_data.has_key('lastname'):
                    id_res_data['nickname'] = id_res_data.get('firstname', '') + ' ' + id_res_data.get('lastname', '')
                elif id_res_data.has_key('email'):
                    id_res_data['nickname'] = id_res_data['email']
            info.ax = id_res_data
        except ax.AXError:
            pass
    return info

############ HANDLERS ##############
class BarrelHouseException(Exception):
    pass

class BarrelHouseFailedVerificationError(BarrelHouseException):
    pass

class BarrelHouseUserNotSetException(BarrelHouseException):
    pass

class AuthOpenIDHandler(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        if environ['PATH_INFO'].startswith(settings.SIGN_IN_URL):
            # Let's load everything into a dict to pass around easier
            auth_prefix = settings.SIGN_IN_URL
            context = Dict(
                    environ=environ,
                    start_response=start_response,
                    body=[]
                    )
            context.base_url = construct_url(
                    environ, with_path_info=False, with_query_string=False
                    )
            context.POST = parse_formvars(environ)
            context.GET = dict(parse_querystring(environ))
            context.session = settings.get_session(environ)
            context.user = settings.get_current_user(environ)
            path = re.sub(auth_prefix, '', environ['PATH_INFO'])
            context.parsed_uri = urlparse.urlparse(path)
            path = context.parsed_uri[2]
            context.continue_url = context.GET.get('continue', None)
            context.openid_begin_url = auth_prefix + '/oid_begin'
            F = types.FunctionType
            defaults = settings.__dict__.iteritems
            context.update(
                    (k,v) for (k,v) in defaults() if not isinstance(v, F)
                    )
            if path == '/' or not path:
                if environ['REQUEST_METHOD'].upper() == 'POST':
                    name = context.POST.get('username')
                    pwd = context.POST.get('password')
                    if not (name and pwd):
                        context.error = True
                        context.message = \
                                settings.USERNAME_OR_PASSWORD_NOT_ENTERED_ERR_MSG
                    else:
                        confirmed = settings.confirm_username_and_password(name, pwd)
                        if not confirmed:
                            context.error = True
                            context.message = \
                                settings.UNRECOGNISED_USERNAME_AND_PASSWORD_ERR_MSG 
                        else:
                            # verified and openid is on the system
                            self.redirect(context, context.continue_url)
                return render_signin(context)
            elif path == '/oid_begin':
                openid_url = context.POST.get('openid_url')
                if not openid_url:
                    return self.redirect(context, auth_prefix)
                else:
                    redirect_url = initiate_openid_login(openid_url, context)
                    #return render_signin(context, error=True, message=redirect_url)
                    return self.redirect(context, redirect_url)
            elif path == '/oid_complete':
                try:
                    response = complete_openid_login(context)
                except FailedOpenIDVerificationError, e:
                    return render_signin(context, error=True, message=e.message)
                info = get_info_from_openid_response(response)
                settings.on_openid_success(info, context)
                if settings.get_current_user(environ) is None:
                    # we have a "pending user" - verified but not registered
                    if not settings.REGISTRATION_URL:
                        # it's up to 'on_openid_success' to set the user if no registration process
                        raise BarrelHouseUserNotSetException()
                    self.redirect(context, regurl)
                else:
                    # verified and openid is on the system
                    self.redirect(context, context.continue_url)
            else:
                return self.not_found(context)
        elif environ['PATH_INFO'].startswith(settings.SIGN_OUT_URL):
            settings.sign_out_current_user(environ)
            context = Dict(start_response=start_response)
            self.redirect(context, '/')
        else:
            return self.app(environ, start_response)

    def redirect(self, context, redirect_url):
        """Send a redirect response to the given URL to the browser."""
        response_headers = [('Content-type', 'text/plain'),
                            ('Location', redirect_url)]
        context.start_response('302 REDIRECT', response_headers)
        return ["Redirecting to %s" % redirect_url]

    def not_found(self, context):
        """Render a page with a 404 return code and a message."""
        fmt = 'The path <strong>%s</strong> was not understood by this server.'
        context['error'] = True
        context['message'] = fmt % (context['parsed_uri'],)
        context['openid_url'] = context.GET.get('openid_url')
        context['status'] = context['title'] = '404 Not Found'
        return settings.render_not_found(context)

########## UTILITY #############
def quoteattr(s):
    qs = cgi.escape(s, 1)
    return '"%s"' % (qs,)

def build_url(context, action, **query):
    """Build a URL relative to the server base_url, with the given
    query parameters added."""
    base = urlparse.urljoin(context['base_url'], settings.SIGN_IN_URL + '/' + action)
    return appendArgs(base, query)

class Dict(object):
    """
    Dict - a dict-alike object
    """
    def __init__(self, **kw):
        self.__dict__.update(kw)

    def __repr__(self):
        return "<Dict %s>" % self.__dict__

    def __getitem__(self, name):
        return self.__dict__[name]

    def __setitem__(self, name, value):
        self.__dict__[name] = value

    def __delitem__(self, name):
        self.__dict__.__delitem__(name)

    def __contains__(self, name):
        return name in self.__dict__

    def __getattr__(self, name):
        return getattr(self.__dict__, name)

    def __setattr__(self, name, value):
        if isinstance(value, types.DictType):
            value = self.__class__(**value)
        object.__setattr__(self, name, value)

    def todict(self):
        return dict(self.__dict__)

