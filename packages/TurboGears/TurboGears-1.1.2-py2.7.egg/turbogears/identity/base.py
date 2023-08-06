"""The TurboGears identity management package."""

# declare what should be exported
__all__ = [
    '_encrypt_password',
    'create_default_provider',
    'current',
    'current_provider',
    'encrypt_password',
    'encrypt_pw_with_algorithm',
    'get_identity_errors',
    'get_failure_url',
    'set_current_identity',
    'set_current_provider',
    'set_identity_errors',
    'set_login_attempted',
    'was_login_attempted',
]


import logging
try:
    from hashlib import md5, sha1
except ImportError:
    from sha import new as sha1
    from md5 import new as md5

import cherrypy
import pkg_resources
import turbogears

from turbogears.util import deprecated, request_available, load_class
from turbogears.identity.exceptions import *


log = logging.getLogger('turbogears.identity')


def create_default_provider():
    """Create default identity provider.

    Creates an identity provider according to what is found in
    the configuration file for the current TurboGears application

    Returns an identity provider instance or
    raises an IdentityConfigurationException.

    """
    provider_plugin = turbogears.config.get('identity.provider', 'sqlobject')
    plugins = pkg_resources.iter_entry_points(
        'turbogears.identity.provider', provider_plugin)

    log.debug("Loading provider from plugin: %s", provider_plugin)

    provider_class = None
    for entrypoint in plugins:
        provider_class = entrypoint.load()
        break

    if not provider_class:
        provider_class = load_class(provider_plugin)

    if not provider_class:
        raise IdentityConfigurationException(
            "IdentityProvider plugin missing: %s" % provider_plugin )
    else:
        return provider_class()

def was_login_attempted():
    try:
        return cherrypy.request.identity_login_attempted
    except AttributeError:
        return False

def set_login_attempted(flag):
    cherrypy.request.identity_login_attempted = flag

def set_current_identity(identity):
    cherrypy.request.identity = identity

    try:
        cherrypy.request.user_name = identity.user_name

    except AttributeError:
        cherrypy.request.user_name = None

def set_current_provider(provider):
    cherrypy.request.identityProvider = provider


def encrypt_pw_with_algorithm(algorithm, password):
    """Hash the given password with the specified algorithm.

    Valid values for algorithm are 'md5' and 'sha1' or 'custom'. If the
    algorithm is 'custom', the config setting 'identity.custom_encryption'
    needs to be set to a dotted-notation path to a callable that takes
    an unencrypted password and gives back the password hash.

    All other algorithms values will be essentially a no-op.

    """
    hashed_password = password
    # The algorithms don't work with unicode objects, so decode first.
    if isinstance(password, unicode):
        password_8bit = password.encode('utf-8')
    else:
        password_8bit = password
    if algorithm == 'md5':
        hashed_password =  md5(password_8bit).hexdigest()
    elif algorithm == 'sha1':
        hashed_password = sha1(password_8bit).hexdigest()
    elif algorithm == 'custom':
        custom_encryption_path = turbogears.config.get(
            'identity.custom_encryption', None)
        if custom_encryption_path:
            custom_encryption = turbogears.util.load_class(
                custom_encryption_path)
        if custom_encryption:
            hashed_password = custom_encryption(password_8bit)
    # Make sure the hashed password is a unicode object at the end of the
    # process, because SQLAlchemy _wants_ that for Unicode columns.
    if not isinstance(hashed_password, unicode):
        hashed_password = hashed_password.decode('utf-8')
    return hashed_password

_encrypt_password = deprecated(
    "Use identity.encrypt_pw_with_algorithm instead."
)(encrypt_pw_with_algorithm)

def encrypt_password(cleartext):
    return current_provider.encrypt_password(cleartext)


class IdentityWrapper(object):
    """A wrapper class for the thread local data.

    This allows developers to access the current user information via
    turbogears.identity.current and get the identity for the current request.

    """

    def identity(self):
        try:
            identity = cherrypy.request.identity

        except AttributeError:
            identity = None

        if not identity:
            if not request_available():
                raise RequestRequiredException()

            raise IdentityManagementNotEnabledException()

        return identity

    def __getattr__(self, name):
        """Return the named attribute of the global state."""
        identity = self.identity()
        if name == '__str__':
            return identity.__str__

        elif name == '__repr__':
            return identity.__repr__

        else:
            return getattr(identity, name)

    def __setattr__(self, name, value):
        """Stash a value in the global state."""
        identity = self.identity()
        setattr(identity, name, value)


class ProviderWrapper(object):

    def __getattr__(self, name):
        try:
            provider = cherrypy.request.identityProvider

        except AttributeError:
            try:
                provider = create_default_provider()
            except Exception, exc:
                log.warning("Could not create default identity provider: %s", exc)
                provider = None

        if provider is None:
            if not request_available():
                raise RequestRequiredException()

            raise IdentityManagementNotEnabledException()

        return getattr(provider, name)

current = IdentityWrapper()
current_provider = ProviderWrapper()
