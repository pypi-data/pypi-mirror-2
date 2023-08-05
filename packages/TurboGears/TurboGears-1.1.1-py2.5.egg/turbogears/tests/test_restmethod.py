# -*- encoding: utf-8 -*-

import cherrypy
import simplejson

from turbogears import expose, testutil
from turbogears.controllers import RESTMethod

__user_registry__ = {}


class UserController(object):

    class default(RESTMethod):

        @expose(format='json')
        def get(self, user_name=None):
            if user_name is None:
                raise cherrypy.NotFound
            user = __user_registry__.get(user_name, None)
            if user is None:
                raise cherrypy.NotFound
            else:
                return user

        @expose(content_type=None)
        def put(self, user_name=None):
            if user_name is None:
                raise cherrypy.NotFound
            if cherrypy.request.headers['Content-Type'] != 'application/json':
                raise cherrypy.HTTPError(
                         415, 'JSON is the only supported format')
            user_details = simplejson.load(cherrypy.request.body)
            __user_registry__[user_name] = user_details
            cherrypy.response.status = '204 No Content'


class RootController(object):

    class users(RESTMethod):

        @expose(format='json')
        def get(self):
            """Return a json formatted list of users"""
            return dict(users=[dict(uri='/'.join(['/user', user_name]),
                                    user_name=user_name,
                                    first_name=user['first_name'],
                                    last_name=user['last_name'])
                        for user_name, user in __user_registry__.items()])

        @expose()
        def post(self):
            """Accept a new user in json format"""
            if cherrypy.request.headers['Content-Type'] != 'application/json':
                raise cherrypy.HTTPError(
                          415, 'JSON is the only supported format')
            user_details = simplejson.load(cherrypy.request.body)
            user_name = user_details.pop('user_name')
            __user_registry__[user_name] = user_details
            cherrypy.response.status = '201 Created'
            new_location = '/'.join(['/user', user_name])
            cherrypy.response.headers['Location'] = new_location
            return "User created.  Please visit %s" % new_location

    user = UserController()


class TestREST(testutil.TGTest):

    root = RootController

    def tearDown(self):
        __user_registry__ = {}

    def test_get_list(self):
        resp = self.app.get('/users').json
        assert resp['users'] == []
        __user_registry__['psr'] = dict(first_name=u'Peter',
                                        last_name=u'Russell')
        resp = self.app.get('/users').json
        assert resp['users'] == [dict(user_name='psr', first_name=u'Peter',
                                      last_name=u'Russell', uri='/user/psr')]

    def test_post(self):
        user = dict(user_name='psr', first_name=u'Peter', last_name=u'Russell')
        resp = self.app.post('/users', simplejson.dumps(user),
                             {'Content-Type': 'application/json'})
        assert __user_registry__['psr'] == dict(first_name=u'Peter',
                                                last_name=u'Russell')

    def test_get_single(self):
        """Positional arguments should still work correctly"""
        __user_registry__['psr'] = dict(first_name=u'Peter',
                                        last_name=u'Russell')
        assert self.app.get('/user/psr').json == __user_registry__['psr']

    def test_put(self):
        __user_registry__['psr'] = dict(first_name=u'Peter',
                                        last_name=u'André')
        user = dict(first_name=u'Peter', last_name=u'Russell')
        self.app.put('/user/psr', simplejson.dumps(user),
                     headers={'Content-Type': 'application/json'})
        assert __user_registry__['psr']['last_name'] == u'Russell'

    def test_unsupported_method(self):
        """Check that we receive a 405 error on deletes"""
        # Really this resource doesn't exist, and so should raise a 404.
        # It's not obvious how to fix this, perhaps by using a different
        # approach to resources than the default method?

        # Note: This test does not work with WebTest 1.2, because it
        # needs one of the following patches:
        # http://trac.pythonpaste.org/pythonpaste/ticket/298 or
        # http://trac.pythonpaste.org/pythonpaste/ticket/316
        # Strangely, with 1.2.1dev it works, even though these
        # patches have not been applied. Needs further investigation.
        return # TODO: investigate and reactivate when WebTest is fixed

        self.app.delete('/user/psr', status=405)

