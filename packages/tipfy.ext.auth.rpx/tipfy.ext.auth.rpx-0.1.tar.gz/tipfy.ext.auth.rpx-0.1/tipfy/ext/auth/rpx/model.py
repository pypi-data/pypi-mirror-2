# -*- coding: utf-8 -*-
"""
    tipfy.ext.auth.rpx
    ~~~~~~~~~~~~~~~~~~

    RPX/JanRain Engage authentication for tipfy.

    :copyright: 2010 Ragan Webber.
    :license: Apache, see LICENSE.txt for more details.
"""

from google.appengine.ext import db
from tipfy.ext.auth.model import User

class Login(db.Model):
    """A RPX login for a user
    """
    #: Creation date.
    created = db.DateTimeProperty(auto_now_add=True)
    #: Modification date.
    updated = db.DateTimeProperty(auto_now=True)
    #: Provider Name
    provider_name = db.StringProperty(required=True)
    #: Name on provider system
    provider_id = db.StringProperty(default=None)
    #: User Reference
    user = db.ReferenceProperty(User)

    @classmethod
    def get_by_login_id(cls, login_id):
        return cls.get_by_key_name(login_id)

    @classmethod
    def get_user_by_login_id(cls, login_id):
        login = cls.get_by_login_id(login_id)
        if login:
            return login.user
        else:
            return None

    @classmethod
    def create(cls, user, login_id, **kwargs):
        """Creates a new user and returns it. If the username already exists,
        returns None.

        :param user:
            User entity
        :param login_id:
            RPX login id
        :param kwargs:
            Additional entity attributes.
        :return:
            The newly created login
        """
        kwargs['user'] = user
        kwargs['key_name'] = login_id
        kwargs['login_id'] = login_id

        def txn():
            login = cls(**kwargs)
            login.put()
            return login

        return db.run_in_transaction(txn)

    def __unicode__(self):
        """Returns username.

        :return:
            Username, as unicode.
        """
        return unicode(self.provider_name)

    def __str__(self):
        """Returns username.

        :return:
            Username, as unicode.
        """
        return self.__unicode__()

    def __eq__(self, obj):
        """Compares this user entity with another one.

        :return:
            ``True`` if both entities have same key, ``False`` otherwise.
        """
        if not obj:
            return False

        return str(self.key()) == str(obj.key())

    def __ne__(self, obj):
        """Compares this user entity with another one.

        :return:
            ``True`` if both entities don't have same key, ``False`` otherwise.
        """
        return not self.__eq__(obj)


