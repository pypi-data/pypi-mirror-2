import unittest
from zope.interface import implements

from islay.auth.interfaces import IChallenger, IIdentifier, IAuthenticator

creds = None

class IslayAuthTestCase(unittest.TestCase):
    pass

# Applications that mimic certain aspects of the authorisation dance

def UnauthorisedApp(environ, start_response):
    headers = []
    headers.append(('WWW-Authenticate', 'Basic realm="WSGI"'))

    start_response("401 Unauthorized", headers)
    return

def ForbiddenApp(environ, start_response):
    headers = []
    start_response("403 Forbidden", headers)
    return

def OKApp(environ, start_response):
    headers = []
    start_response("200 OK", headers)
    return

def UsernameApp(environ, start_response):
    headers = []
    start_response("200 OK", headers)

    return [environ.get('REMOTE_USER', ''), ]

# Fake plugins we can use to make life easy

class StaticTextChallenger(object):
    implements(IChallenger)
    
    def challenge(self, environ, status, app_headers, forget_headers):
        def ChallengeApp(environ, start_response):
            headers = [("Content-type", "text/plain"), ]
            start_response("200 OK", headers)
            return ["Who do you think you are?", ]
        return ChallengeApp


class GlobalNoteRemoteUser(object):
    implements(IIdentifier)
    
    def identify(self, environ):
        global creds
        try:
            creds = {'user':environ['REMOTE_USER'], }
        except KeyError:
            return None
        
        return creds
    
    def remember(self, environ, identity):
        return
    
    def forget(self, environ, identity):
        return


class isLowerCase(object):
    implements(IAuthenticator)

    def authenticate(self, environ, identity):
        if identity.get('user', "NONE").islower():
            return identity['user']
        else:
            return None


# Constants

MINIMAL_REQUEST = {'HTTP_HOST':'example', 
                   'wsgi.url_scheme':'http',
                   'PATH_INFO':'/',
                   'REQUEST_METHOD':'GET'}