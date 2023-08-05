from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from userena import views as userena_views
from userena import settings as userena_settings

urlpatterns = patterns('',
                       # Inactive user
                       url(r'^disabled/$',
                           direct_to_template,
                           {'template': 'userena/disabled.html'},
                           name='userena_disabled'),

                       # Activate
                       url(r'^activation/complete/$',
                           direct_to_template,
                           {'template': 'userena/activation_complete.html'},
                           name='userena_activation_complete'),
                       url(r'^verify/(?P<activation_key>\w+)/$',
                           userena_views.activate,
                           name='userena_activate'),

                       # Signin, signout and signup
                       url(r'^signin/$',
                           userena_views.signin,
                           name='userena_signin'),
                       url(r'^signout/$',
                           auth_views.logout,
                           {'template_name': 'userena/signout.html'},
                           name='userena_signout'),
                       url(r'^signup/$',
                           userena_views.signup,
                           name='userena_signup'),
                       url(r'^signup/complete/$',
                           direct_to_template,
                           {'template': 'userena/signup_complete.html',
                            'extra_context': {'userena_verification_days': userena_settings.USERENA_ACTIVATION_DAYS}},
                           name='userena_signup_complete'),

                       # Reset password
                       url(r'^password/reset/$',
                           auth_views.password_reset,
                           {'template_name': 'userena/password_reset_form.html',
                            'email_template_name': 'userena/emails/password_reset_message.txt'},
                           name='userena_password_reset'),
                       url(r'^password/reset/done/$',
                           auth_views.password_reset_done,
                           {'template_name': 'userena/password_reset_done.html'},
                           name='userena_password_reset_done'),
                       url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
                           auth_views.password_reset_confirm,
                           {'template_name': 'userena/password_reset_confirm_form.html'},
                           name='userena_password_reset_confirm'),
                       url(r'^password/reset/confirm/complete/$',
                           auth_views.password_reset_complete,
                           {'template_name': 'userena/password_reset_complete.html'}),

                       # Account settings
                       url(r'^(?P<username>\w+)/password/$',
                           auth_views.password_change,
                           {'template_name': 'userena/password_form.html'},
                           name='userena_password_change'),
                       url(r'^(?P<username>\w+)/password/complete/$',
                           auth_views.password_change_done,
                           {'template_name': 'userena/password_complete.html'},
                           name='userena_password_change_complete'),
                       url(r'^(?P<username>\w+)/email/$',
                           userena_views.email_change,
                           name='userena_email_change'),
                       url(r'^(?P<username>\w+)/email/complete/$',
                           direct_to_template,
                           {'template': 'userena/me_email_complete.html'},
                           name='userena_email_complete'),
                       url(r'^(?P<username>\w+)/$',
                           userena_views.detail,
                           name='userena_detail'),
                        url(r'^$',
                            userena_views.list,
                            name='userena_list'),
 )
