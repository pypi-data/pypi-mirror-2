import webob

from islay.auth.auth import AuthFactory

from islay.auth.tests.base import IslayAuthTestCase
from islay.auth.tests.base import OKApp, UsernameApp
from islay.auth.tests.base import MINIMAL_REQUEST
import islay.auth.tests.base

class TestIdentifiers(IslayAuthTestCase):
    
    def setUp(self):
        environ = MINIMAL_REQUEST.copy()
        environ.update({'REMOTE_USER':'example'})
        self.request = webob.Request(environ)
        self.ok = OKApp
        self.app = AuthFactory({}, identifier='islay.auth.tests.base.GlobalNoteRemoteUser',)(self.ok)
        islay.auth.tests.base.creds = None

    def test_app_is_ok(self):
        response = self.request.get_response(self.app)
        self.assertEqual(response.status, '200 OK')
    
    def test_app_stores_creds(self):
        response = self.request.get_response(self.app)
        self.assertEqual(islay.auth.tests.base.creds, {'user':'example'})

class TestAuthenticators(IslayAuthTestCase):
    def setUp(self):
        self.environ = MINIMAL_REQUEST.copy()
        self.app = UsernameApp
        self.app = AuthFactory({}, identifier='islay.auth.tests.base.GlobalNoteRemoteUser',
                                   authenticator='islay.auth.tests.base.isLowerCase')(self.app)
        islay.auth.tests.base.creds = None

    def test_lowercase_has_user(self):
        self.environ.update({'REMOTE_USER':'example'})
        request = webob.Request(self.environ)
        
        response = request.get_response(self.app)
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.body, 'example')
    
    def test_uppercase_has_no_user(self):
        self.environ.update({'REMOTE_USER':'EXAMPLE'})
        request = webob.Request(self.environ)
        
        response = request.get_response(self.app)
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.body, '')