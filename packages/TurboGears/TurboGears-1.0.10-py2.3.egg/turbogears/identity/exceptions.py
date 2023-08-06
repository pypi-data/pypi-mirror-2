"""Identity management exceptions."""


import cherrypy
import turbogears


def set_identity_errors(errors):
    if isinstance(errors, basestring):
        errors = [errors]
    cherrypy.request.identity_errors = list(errors)

def get_identity_errors():
    return getattr(cherrypy.request, 'identity_errors', [])

def get_failure_url(errors=None):
    url = turbogears.config.get('identity.failure_url', None)
    if url is None:
        msg = "Missing URL for identity failure. Please fix this in app.cfg."
        raise IdentityConfigurationException(msg)
    if callable(url):
        url = url(errors)
    return url

class IdentityException(Exception):
    """Base class for all Identity exceptions."""
    pass


class RequestRequiredException(IdentityException):
    """No request present.

    An attempt was made to use a facility of Identity that requires the
    presence of an HTTP request.

    """

    def __str__(self):
        return "An attempt was made to use a facility of the TurboGears " \
            "Identity Management framework that relies on an HTTP request " \
            "outside of a request."


class IdentityManagementNotEnabledException(IdentityException):
    """User forgot to enable Identity management."""

    def __str__(self):
        return "An attempt was made to use a facility of the TurboGears " \
            "Identity Management framework, but identity management hasn't " \
            "been enabled in the config file [via identity.on]."


class IdentityConfigurationException(IdentityException):
    """Incorrect configuration.

    Exception thrown when the Identity management system hasn't been configured
    correctly. Mostly, when failure_url is not specified.

    """

    args = ()

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class IdentityFailure(cherrypy.InternalRedirect, IdentityException):
    """Identity failure.

    Exception thrown when an access control check fails.

    """

    def __init__(self, errors):
        """Setup identity errors on the request and get URL from config."""
        set_identity_errors(errors)
        url = get_failure_url(errors)
        if turbogears.config.get('identity.force_external_redirect', False):
            # We need to use external redirect for https since we are managed
            # by Apache/nginx or something else that CherryPy won't find.
            # We also need to set the forward_url, because the Referer header
            # won't work with an external redirect.
            params = cherrypy.request.original_params
            params['forward_url'] = cherrypy.request.path_info
            raise cherrypy.HTTPRedirect(turbogears.url(url, params))
        else:
            # use internal redirect which is quicker
            cherrypy.InternalRedirect.__init__(self, url)
