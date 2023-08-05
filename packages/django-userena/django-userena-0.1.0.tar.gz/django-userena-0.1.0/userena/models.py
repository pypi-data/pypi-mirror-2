from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.utils.hashcompat import sha_constructor
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.core.exceptions import ImproperlyConfigured

from userena import settings as userena_settings
from userena.utils import get_gravatar

import datetime, random, re
from dateutil.relativedelta import relativedelta
from easy_thumbnails.fields import ThumbnailerImageField

SHA1_RE = re.compile('^[a-f0-9]{40}$')

def upload_to_mugshot(instance, filename):
    """
    Uploads a mugshot for a user to the ``USERENA_MUGSHOT_PATH`` and creating a
    unique hash for the image. This is for privacy reasons so others can't just
    browse through the mugshot directory.

    """
    extension = filename.split('.')[-1]
    salt = sha_constructor(str(random.random())).hexdigest()[:5]
    hash = sha_constructor(salt+str(instance.user.id)).hexdigest()[:10]
    return '%(path)s%(hash)s.%(extension)s' % {'path': userena_settings.USERENA_MUGSHOT_PATH,
                                               'hash': hash,
                                               'extension': extension}

class AccountManager(models.Manager):
    """ Extra functionality for the account manager. """

    def create_inactive_user(self, username, email, password):
        """
        A simple wrapper that creates a new ``User`` and a new ``Account``.

        """
        new_user = User.objects.create_user(username, email, password)
        new_user.is_active = False
        new_user.save()

        # Create account also
        account = self.create_account(new_user)

        return new_user

    def create_account(self, user):
        """
        Create an ``Account`` for a given ``User``.

        Also creates a ``activation_key`` for this account. After the account
        is created an e-mail is send with ``send_activation_email`` to the
        user with this key.

        """
        salt = sha_constructor(str(random.random())).hexdigest()[:5]
        username = user.username
        if isinstance(username, unicode):
            username = username.encode('utf-8')
        activation_key = sha_constructor(salt+username).hexdigest()
        account = self.create(user=user,
                              activation_key=activation_key,
                              activation_key_created=datetime.datetime.now())
        account.send_activation_email()
        return account

    def activate_user(self, activation_key):
        """
        Activate an ``Account`` by supplying a valid ``activation_key``.

        If the key is valid and an account is found, activate the user and
        return the activied account.

        """
        if SHA1_RE.search(activation_key):
            try:
                account = self.get(activation_key=activation_key)
            except self.Model.DoesNotExist:
                return False
            if not account.activation_key_expired():
                account.activation_key = userena_settings.USERENA_ACTIVATED
                account.user.is_active=True
                account.save()
                return account
        return False

    def notify_almost_expired(self):
        """
        Check for accounts that are ``USERENA_ACTIVATED_NOTIFY_DAYS`` days
        before expiration. For each account that's found
        ``send_expiry_notification`` is called.

        Returns a list of all the accounts that have received a notification.

        """
        if userena_settings.USERENA_ACTIVATION_NOTIFY:
            expiration_date = datetime.datetime.now() - datetime.timedelta(days=(userena_settings.USERENA_ACTIVATION_DAYS - userena_settings.USERENA_ACTIVATION_NOTIFY_DAYS))

            accounts = self.filter(user__is_active=False,
                                   user__is_staff=False,
                                   activation_notification_send=False)
            notified_accounts = []
            for account in accounts:
                if account.activation_key_almost_expired():
                    account.send_expiry_notification()
                    notified_accounts.append(account)
            return notified_accounts

    def delete_expired_users(self):
        """
        Checks for expired accounts and delete's the ``User`` associated with
        it. Skips if the user ``is_staff``.

        Returns a list of the deleted accounts.

        """
        deleted_users = []
        for account in self.filter(user__is_staff=False):
            if account.activation_key_expired():
                deleted_users.append(account.user)
                account.user.delete()
        return deleted_users

class BaseAccount(models.Model):
    """
    A user account which stores all the nescessary information to have a full
    functional user implementation on your Django website.

    """
    MUGSHOT_SETTINGS = {'size': (userena_settings.USERENA_MUGSHOT_SIZE,
                                 userena_settings.USERENA_MUGSHOT_SIZE),
                        'crop': 'smart'}
    GENDER_CHOICES = (
        (1, _('Male')),
        (2, _('Female')),
    )

    user = models.ForeignKey(User, unique=True, verbose_name=_('user'))
    mugshot = ThumbnailerImageField(_('mugshot'),
                                    blank=True,
                                    upload_to=upload_to_mugshot,
                                    resize_source=MUGSHOT_SETTINGS,
                                    help_text=_('A personal image displayed in your profile.'))
    gender = models.PositiveSmallIntegerField(_('gender'),
                                              choices=GENDER_CHOICES,
                                              blank=True,
                                              null=True)
    website = models.URLField(_('website'), blank=True, verify_exists=True)
    location =  models.CharField(_('location'), max_length=255, blank=True)
    birth_date = models.DateField(_('birth date'), blank=True, null=True)
    about_me = models.TextField(_('about me'), blank=True)

    # Fields used for managing accounts
    last_active = models.DateTimeField(null=True, blank=True)

    activation_key = models.CharField(_('activation key'), max_length=40,
                                        blank=True)
    activation_key_created = models.DateTimeField(_('creation date of activation key'),
                                                  blank=True,
                                                  null=True)
    activation_notification_send = models.BooleanField(_('notification send'),
                                                       default=False,
                                                       help_text=_('Designates whether this user has already got a notification about activating their account.'))

    # To change their e-mail address, they first have to verify it.
    temporary_email = models.EmailField(_('temporary_email'),
                                        blank=True,
                                        help_text=_('Temporary email address when the user requests an email change.'))

    objects = AccountManager()

    class Meta:
        if userena_settings.USERENA_CHILD_MODEL:
            abstract = True

    def __unicode__(self):
        return '%s' % self.user

    @models.permalink
    def get_absolute_url(self):
        return ('userena_detail', (), {'username': self.user.username})

    @property
    def activity(self):
        """
        Returning the activity of the user

        @TIP: http://www.arnebrodowski.de/blog/482-Tracking-user-activity-with-Django.html

        """
        pass

    @property
    def age(self):
        """ Returns integer telling the age in years for the user """
        today = datetime.date.today()
        return relativedelta(today, self.birth_date).years

    def change_email(self, email):
        """
        Changes the e-mail address for a user.

        A user needs to verify this new e-mail address before it becomes
        active. By storing there new e-mail address in a temporary field --
        ``temporary_email`` -- we are able to set this e-mail address after the
        user has verified it by clicking on the activation URI in the
        activation e-mail. This e-mail get's send by
        ``send_activation_email``.

        """
        # Email is temporary until verified
        self.temporary_email = email

        # New activation key
        salt = sha_constructor(str(random.random())).hexdigest()[:5]
        self.activation_key = sha_constructor(salt+self.user.username).hexdigest()
        self.activation_key_created = datetime.datetime.now()

        # Send email for activation
        self.send_activation_email(new_email=True)
        self.save()

    @property
    def get_activation_url(self):
        """ Simplify it to get the activation URI """
        site = Site.objects.get_current()
        path = reverse('userena_activate',
                       kwargs={'activation_key': self.activation_key})
        return 'http://%(domain)s%(path)s' % {'domain': site.domain,
                                              'path': path}

    def activation_key_expired(self):
        """
        Returns ``True`` when the ``activation_key`` of the account is
        expired and ``False`` if the key is still valid.

        The key is either expired when the key is set to the value defined in
        ``USERENA_ACTIVATED`` or ``activation_key_created`` is beyond the
        amount of days defined in ``USERENA_ACTIVATION_DAYS``.

        """
        expiration_days = datetime.timedelta(days=userena_settings.USERENA_ACTIVATION_DAYS)
        if self.activation_key == userena_settings.USERENA_ACTIVATED:
            return True
        if datetime.datetime.now() >= self.activation_key_created + expiration_days:
            return True
        return False

    def activation_key_almost_expired(self):
        """
        Returns ``True`` when the ``activation_key`` is almost expired.

        A key is almost expired when the there are less than
        ``USERENA_ACTIVATION_NOTIFY_DAYS`` days left before expiration.

        """
        notification_days = datetime.timedelta(days=(userena_settings.USERENA_ACTIVATION_DAYS - userena_settings.USERENA_ACTIVATION_NOTIFY_DAYS))
        if datetime.datetime.now() >= self.activation_key_created + notification_days:
            return True
        return False

    def send_activation_email(self):
        """
        Sends a activation e-mail to the user.

        This e-mail is send when the user wants to activate their newly created
        account.

        """
        # Which templates to use, either for a new account, or for a e-mail
        # address change.
        context= {'account': self,
                  'activation_days': userena_settings.USERENA_ACTIVATION_DAYS,
                  'site': Site.objects.get_current()}

        subject = render_to_string('userena/emails/activation_email_subject.txt', context)
        subject = ''.join(subject.splitlines())

        message = render_to_string('userena/emails/activation_email_subject.txt', context)
        send_mail(subject,
                  message,
                  settings.DEFAULT_FROM_EMAIL,
                  [self.user.email,])

    def send_expiry_notification(self):
        """
        Notify the user that his account is about to expire.

        Sends an e-mail to the user telling them that their account is
        ``USERENA_ACTIVATION_NOTIFY_DAYS`` away before expiring.

        """
        context = {'account': self,
                   'days_left': userena_settings.USERENA_ACTIVATION_NOTIFY_DAYS,
                   'site': Site.objects.get_current()}

        subject = render_to_string('userena/emails/activation_notify_subject.txt',
                                   context)
        subject = ''.join(subject.splitlines())

        message = render_to_string('userena/emails/activation_notify_message.txt',
                                   context)

        self.user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL)
        self.activation_notification_send = True
        self.save()

    def get_mugshot_url(self):
        """
        Returns the image containing the mugshot for the user. This can either
        an uploaded image or a Gravatar.

        Gravatar functionality will only be used when
        ``USERENA_MUGSHOT_GRAVATAR`` is set to ``True``.

        Return ``None`` when Gravatar is not used and no default image is
        supplied by ``USERENA_MUGSHOT_DEFAULT``.

        """
        # First check for a mugshot and if any return that.
        if self.mugshot:
            return self.mugshot.url

        # Use Gravatar if the user wants to.
        if userena_settings.USERENA_MUGSHOT_GRAVATAR:
            return get_gravatar(self.user.email,
                                userena_settings.USERENA_MUGSHOT_SIZE,
                                userena_settings.USERENA_MUGSHOT_DEFAULT)

        # Gravatar not used, check for a default image. Don't use the gravatar defaults
        else:
            if userena_settings.USERENA_MUGSHOT_DEFAULT not in ['404', 'mm', 'identicon', 'monsterid', 'wavatar']:
                return userena_settings.USERENA_MUGSHOT_DEFAULT
            else: return None

def get_account_model():
    """
    Returns the right account model so your user application can be easily
    extended without adding extra relationships.

    """
    from django.db.models import get_model
    if userena_settings.USERENA_CHILD_MODEL:
        account_model = get_model(*userena_settings.USERENA_CHILD_MODEL.split('.', 2))
        if not account_model:
            raise ImproperlyConfigured('Cannot find the model defined in ``USERINA_CHILD_MODEL``.')
        return account_model

    return BaseAccount

# Return the model that's used for account functionality
Account = get_account_model()

# Always return an account when asked through a user
User.account = property(lambda u: Account.objects.get_or_create(user=u)[0])
