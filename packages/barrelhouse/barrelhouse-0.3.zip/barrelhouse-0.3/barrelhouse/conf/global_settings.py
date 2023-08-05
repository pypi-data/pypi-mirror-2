
from liberet import Delayed, Required

__MODULE__ = 'settings.barrelhouse'

SIGN_IN_URL = '/accounts/signin'
SIGN_OUT_URL = '/accounts/signout'
FORGOT_PASSWORD_URL = '/accounts/sendpw'
REGISTRATION_URL = None
SESSION_USER_KEY = 'barrelhouse.user'

UNRECOGNISED_USERNAME_AND_PASSWORD_ERR_MSG = \
    'Unrecognised username and password.'
USERNAME_OR_PASSWORD_NOT_ENTERED_ERR_MSG = \
    'Please enter a username and password.'
# list of attributes to request via Simple Registration
OPENID_SREG_ATTRS = ['nickname', 'email']

# dict of uris => attributes to request via Attribute Exchange
OPENID_AX_ATTRS = {
    'http://axschema.org/contact/email':        'email',
    'http://axschema.org/namePerson/friendly':  'nickname',
    'http://axschema.org/namePerson/first':     'firstname',
    'http://axschema.org/namePerson/last':      'lastname',
}

# openid
consumer_class = None
get_session = Required
get_store = Required

# rendering
render_signin = Required
render_signout = Required

# handlers
on_openid_success = Required
confirm_username_and_password = Required

get_current_user = Delayed('barrelhouse.get_current_user')
set_current_user = Delayed('barrelhouse.set_current_user')
sign_out_current_user = Delayed('barrelhouse.sign_out_current_user')

#def url_to_username(environ, openid_url):
#    return openid_url

