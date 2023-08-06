from django.db import models
from django.db.models import Q
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import User, AnonymousUser

from userena import settings as userena_settings
from userena.utils import generate_sha1, get_profile_model

from guardian.shortcuts import assign, get_perms

import re, datetime

SHA1_RE = re.compile('^[a-f0-9]{40}$')

PERMISSIONS = {
    'profile': ('view_profile', 'change_profile'),
    'user': ('change_user', 'delete_user')
}

class UserenaManager(UserManager):
    """ Extra functionality for the Userena model. """

    def create_inactive_user(self, username, email, password):
        """
        A simple wrapper that creates a new ``User``.

        """
        now = datetime.datetime.now()

        new_user = User.objects.create_user(username, email, password)
        new_user.is_active = False
        new_user.save()

        userena_profile = self.create_userena_profile(new_user)

        # All users have an empty profile
        profile_model = get_profile_model()
        new_profile = profile_model(user=new_user)
        new_profile.save(using=self._db)

        # Give permissions to view and change profile
        for perm in PERMISSIONS['profile']:
            assign(perm, new_user, new_profile)

        # Give permissinos to view and change itself
        for perm in PERMISSIONS['user']:
            assign(perm, new_user, new_user)

        userena_profile.send_activation_email()

        return new_user

    def create_userena_profile(self, user):
        """ Creates an userena profile """
        if isinstance(user.username, unicode):
            user.username = user.username.encode('utf-8')
        salt, activation_key = generate_sha1(user.username)

        return self.create(user=user,
                           activation_key=activation_key)

    def activate_user(self, username, activation_key):
        """
        Activate an ``User`` by supplying a valid ``activation_key``.

        If the key is valid and an user is found, activate the user and
        return it.

        """
        if SHA1_RE.search(activation_key):
            try:
                userena = self.get(user__username=username,
                                   activation_key=activation_key)
            except self.model.DoesNotExist:
                return False
            if not userena.activation_key_expired():
                userena.activation_key = userena_settings.USERENA_ACTIVATED
                user = userena.user
                user.is_active = True
                userena.save(using=self._db)
                user.save(using=self._db)
                return user
        return False

    def confirm_email(self, username, confirmation_key):
        """
        Confirm an email address by checking a ``confirmation_key``.

        A valid ``confirmation_key`` will set the newly wanted e-mail address
        as the current e-mail address. Returns the user after success or
        ``False`` when the confirmation key is invalid.

        """
        if SHA1_RE.search(confirmation_key):
            try:
                userena = self.get(user__username=username,
                                   email_confirmation_key=confirmation_key,
                                   email_unconfirmed__isnull=False)
            except self.model.DoesNotExist:
                return False
            else:
                user = userena.user
                user.email = userena.email_unconfirmed
                userena.email_unconfirmed, userena.email_confirmation_key = '',''
                userena.save(using=self._db)
                user.save(using=self._db)
                return user
        return False

    def delete_expired_users(self):
        """
        Checks for expired users and delete's the ``User`` associated with
        it. Skips if the user ``is_staff``.

        Returns a list of the deleted users.

        """
        deleted_users = []
        for user in User.objects.filter(is_staff=False,
                                        is_active=False):
            if user.userena_signup.activation_key_expired():
                deleted_users.append(user)
                user.delete()
        return deleted_users

    def check_permissions(self):
        """
        Checks that all permissions are set correctly for the users.

        Returns a set of users whose permissions was wrong.

        """
        changed_users = set()
        for user in User.objects.all():
            if not user.username == 'AnonymousUser':
                all_permissions = get_perms(user, user.get_profile()) + get_perms(user, user)

                for model, perms in PERMISSIONS.items():
                    if model == 'profile':
                        perm_object = user.get_profile()
                    else: perm_object = user

                    for perm in perms:
                        if perm not in all_permissions:
                            assign(perm, user, perm_object)
                            changed_users.add(user)

        return changed_users

class UserenaBaseProfileManager(models.Manager):
    """ Manager for UserenaProfile """
    def get_visible_profiles(self, user=None):
        """
        Returns all the visible profiles available to this user.

        For now keeps it simple by just applying the cases when a user is not
        active, a user has it's profile closed to everyone or a user only
        allows registered users to view their profile.

        **Keyword Arguments**

        ``user``
            A django ``User`` instance.

        """
        profiles = self.all()

        filter_kwargs = {'user__is_active': True}

        profiles = profiles.filter(**filter_kwargs)
        if user and isinstance(user, AnonymousUser):
            profiles = profiles.exclude(Q(privacy='closed') | Q(privacy='registered'))
        else: profiles = profiles.exclude(Q(privacy='closed'))
        return profiles
