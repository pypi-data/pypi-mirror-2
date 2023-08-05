# -*- coding: utf-8 -*-
"""
    tipfy.ext.auth.rpx
    ~~~~~~~~~~~~~~~~~~

    RPX/JanRain Engage authentication for tipfy.

    :copyright: 2010 Ragan Webber.
    :license: Apache, see LICENSE.txt for more details.
"""

import urllib
from google.appengine.api import urlfetch
from django.utils import simplejson as json
from tipfy import (REQUIRED_VALUE, get_config, url_for)
from tipfy.ext.auth import MultiAuthMixin
import logging
from model import Login

default_config = {
    'api_key': REQUIRED_VALUE,
    'application_domain': REQUIRED_VALUE,
}

def get_callback_url(_continue = '/'):
    token_url = "%s?continue=%s" % (url_for('auth/rpx', full=True), _continue)
    token_url = urllib.quote_plus(token_url)
    rpx_url = get_config('tipfy.ext.auth.rpx', 'application_domain')
    return "%s/openid/v2/signin?token_url=%s" % (rpx_url, token_url)


class RPXMixin(MultiAuthMixin):
    def _rpx_api_key(self):
        return self.app.get_config(__name__, 'api_key')

    def _rpx_application_domain(self):
        return self.app.get_config(__name__, 'application_domain')

    def get_authenticated_user(self, callback):
        token = self.request.form.get('token')
        url = 'https://rpxnow.com/api/v2/auth_info'
        args = {
            'format': 'json',
            'apiKey': self._rpx_api_key(),
            'token': token,
        }

        try:
            response = urlfetch.fetch(url=url,
                               payload=urllib.urlencode(args),
                               method=urlfetch.POST,
                               headers={'Content-Type':'application/x-www-form-urlencoded'},
                               deadline=10
                              )
            if response.status_code < 200 or response.status_code >= 300:
                logging.warning('Invalid RPX Token Fetch response: %s',
                    response.content)
                response = None
        except urlfetch.DownloadError, e:
            logging.exception(e)
            response = None

        return self._on_response(response, callback)

    def _on_response(self, response, callback):
        rpx_response = json.loads(response.content)

        if rpx_response['stat'] == 'ok':
            profile = rpx_response['profile']
            login_id = profile.get('identifier')
            username = profile.get('preferredUsername', '')
            email = profile.get('email', '')
            data = {
                'login_id': login_id,
                'username': username,
                'email': email,
                'provider_name': profile.get('providerName'),
                'provider_id': username or email or profile.get('displayName', '')
            }
            return callback(data)
        else:
            return callback(None)

    def auth_create_login(self, user=None, login_id=None, **kwargs):
        logging.info("Creating login '%s' for user '%s'" % (login_id, user))
        login = Login.create(user, login_id, **kwargs)
        login.put()
        return login

    def auth_login_with_third_party(self, auth_id=None, login_id=None, remember=False, **kwargs):
        """Called to authenticate the user after a third party confirmed
        authentication.

        :param login_id:
            Authentication id, generally a combination of service name and
            user identifier for the service, e.g.: 'twitter:john'.
        :param remember:
            True if authentication should be persisted even if user leaves the
            current session (the "remember me" feature).
        :return:
            ``None``. This always authenticates the user.
        """
        # Load user entity.
        user = self.auth_get_user_entity(login_id=login_id)
        if user:
            # Set current user from datastore.
            self.auth_set_session(user.auth_id, user.session_id, remember,
                **kwargs)
        else:
            # Simply set a session; user will be created later if required.
            self.auth_set_session(auth_id, remember=remember, login_id=login_id, **kwargs)
        return user

    def auth_get_user_entity(self, username=None, auth_id=None, login_id=None):
        """Loads an user entity from datastore. Override this to implement
        a different loading method. This method will load the user depending
        on the way the user is being authenticated: for form authentication,
        username is used; for third party or App Engine authentication,
        auth_id is used.

        :param username:
            Unique username.
        :param auth_id:
            Unique authentication id.
        :return:
            A ``User`` model instance, or ``None``.
        """
        if auth_id:
            return self.auth_user_model.get_by_auth_id(auth_id)
        elif login_id:
            return Login.get_user_by_login_id(login_id)
        elif username:
            return self.auth_user_model.get_by_username(username)

