django-apikey
=============
Key authentication for django. Can be used with django-piston easily.

Based on https://github.com/scoursen/django-apikey.


Installation
------------
::

    pip install django-apikey


Configuration
-------------

Add 'apikey' to your settings.py:
::

    INSTALLED_APPS = (
    ...
    'apikey',
    ....
    )

A Question
----------

What is a Token and a Key? and which are the differences between them?

Token
.....

A Token is generated with::

    Token.objects.create(user)

and it can be used to authenticate requests with Django-Piston as long as it remain active, which is configured in settings.py::

    TOKEN_VALID_SECONDS = 3600

The header used to send the token is configured in settings.py with::

    TOKEN_AUTH_HEADER = 'X-Auth-Token'

To ask for a token in a resource handler use it like this::

    from apikey.auth import TokenAuthentication
    from piston.handler import BaseHandler
    from piston.resource import Resource
    from app.models import Item
    
    class ItemHandler(BaseHandler):
        allowed_methods = ('GET', )
	fields = ('name', 'id')
        model = Item
    
        def read(self, request):
            return Item.objects.all()
    
    handler = Resource(
        handler=ItemHandler, authentication=TokenAuthentication())
   
The token remains active TOKEN_VALID_SECONDS after each request, and it should be created in a request authenticated with the username/email and password/key, or Basic, Digest.


ApiKey
......

ApiKey is basically a key used to authenticate the requests that replace an email/username and password in all the API request.

You can change the authorization header by setting the APIKEY_AUTHORIZATION_HEADER in settings.py:
::

    APIKEY_AUTHORIZATION_HEADER = 'App-Authorization'


To add api authentication with piston write this in your handlers::

    from apikey.auth import ApiKeyAuthentication
    from piston.handler import BaseHandler
    from piston.resource import Resource
    from app.models import Item
    
    class ItemHandler(BaseHandler):
        allowed_methods = ('GET', )
	fields = ('name', 'id')
        model = Item
    
        def read(self, request):
            return Item.objects.all()
    
    handler = Resource(
        handler=ItemHandler, authentication=ApiKeyAuthentication())


Thanks
------

This project is base on the one of Steve Coursen https://github.com/scoursen/django-apikey but with several simplifications, and adds.

License
-------

This software is licensed  under the New BSD License.
