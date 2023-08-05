# Copyright (c) 2010, Matthew Wilkess
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the Matthew Wilkes nor his employers nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from webob import Request, Response

def importFromName(path):
    parts = path.split('.')
    outer = '.'.join(parts[:-1])
    args = outer, globals(), locals(), parts[-1]
    module = __import__(*args)
    return getattr(module, parts[-1])

def AuthFactory(global_config, **local_conf):
    
    identifiers = []
    authenticators = []
    challengers = []
    
    for path in local_conf.get('identifier', '').split(','):
        if path:
            identifiers.append(importFromName(path))

    for path in local_conf.get('authenticator', '').split(','):
        if path:
            authenticators.append(importFromName(path))

    for path in local_conf.get('challenger', '').split(','):
        if path:
            challengers.append(importFromName(path))

    
    class AuthMiddleware(object):
        """An endpoint"""
    
        def __init__(self, app):
            self.app = app
            self.identifiers = identifiers
            self.authenticators = authenticators
            self.challengers = challengers            
    
        def __call__(self, environ, start_response):
            request = Request(environ)

            auth = None
            identifier = None

            for identifier in self.identifiers:
                identifier = identifier()
                credentials = identifier.identify(environ)
                if credentials is None:
                    continue
                else:
                    for authenticator in authenticators:
                        auth = authenticator().authenticate(environ, credentials)
                        if auth is None:
                            continue
                        else:
                            break
            
            if auth:
                request.environ['REMOTE_USER'] = auth
            elif 'REMOTE_USER' in request.environ:
                del request.environ['REMOTE_USER']
            
            response = request.get_response(self.app)

            if response.status == '401 Unauthorized':
                for challenger in self.challengers:
                    if identifier is not None:
                        forget_headers = identifier.forget(environ, credentials)
                    else:
                        forget_headers = []
                    challenge = challenger().challenge(environ, 
                                                       response.status, 
                                                       response.headers, 
                                                       forget_headers)
                    if challenge is None:
                        continue
                    else:
                        return challenge(environ, start_response)
            else:
                if identifier is not None:
                    response.headers.update(identifier.remember(environ, credentials))
                return response(environ, start_response)
    
    return AuthMiddleware

AuthMiddleware = AuthFactory({}) # Generic version without config