
import liberet
render_template = liberet.Delayed('djinn.render_template')

## barrelhouse settings
_beaker_environ_key = 'barrelhouse.beaker.session'
SESSION_USER_KEY = 'barrelhouse.demo.user'

def get_store():
    return AppEngineStore()

def get_session(environ):
    return environ.get(_beaker_environ_key)

def render_signin(context):
    return render_template('signin.html', context.todict())

def render_signout(context):
    pass

def on_openid_success(info, context):
    session = get_session(context.environ)
    session[SESSION_USER_KEY] = info['claimed_id']
    session.save()

def confirm_username_and_password(username, password):
    return False

def sign_out_current_user(environ):
    session = get_session(environ)
    session.delete()

#below from aeoid
from google.appengine.api import memcache
from openid.association import Association as OpenIDAssociation
from openid.store import interface
from openid.store import nonce

MEMCACHE_NAMESPACE = "barrelhouse"

# from http://github.com/arachnid/aeoid
class AppEngineStore(interface.OpenIDStore):
    def getAssociationKeys(self, server_url, handle):
        return ("assoc:%s" % (server_url,),
                        "assoc:%s:%s" % (server_url, handle))

    def storeAssociation(self, server_url, association):
        data = association.serialize()
        key1, key2 = self.getAssociationKeys(server_url, association.handle)
        memcache.set_multi({key1: data, key2: data},
                                             namespace=MEMCACHE_NAMESPACE)

    def getAssociation(self, server_url, handle=None):
        key1, key2 = self.getAssociationKeys(server_url, handle)
        if handle:
            results = memcache.get_multi([key1, key2], namespace=MEMCACHE_NAMESPACE)
        else:
            results = {key1: memcache.get(key1, namespace=MEMCACHE_NAMESPACE)}
        data = results.get(key2) or results.get(key1)
        if data:
            return OpenIDAssociation.deserialize(data)
        else:
            return None

    def removeAssociation(self, server_url, handle):
        key1, key2 = self.getAssociationKeys(server_url, handle)
        return memcache.delete(key2) == 2

    def useNonce(self, server_url, timestamp, salt):
        nonce_key = "nonce:%s:%s" % (server_url, salt)
        expires_at = timestamp + nonce.SKEW
        return memcache.add(nonce_key, None, time=expires_at,
                                                namespace=MEMCACHE_NAMESPACE)
