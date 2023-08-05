
import liberet

from barrelhouse.conf import global_settings as defaults

modname = getattr(defaults, '__MODULE__', None)
prefix = getattr(defaults, '__PREFIX__', None)

settings = liberet.get_config_handle(modname, prefix)

if not settings:
    settings = liberet.register(defaults, modname, prefix)

