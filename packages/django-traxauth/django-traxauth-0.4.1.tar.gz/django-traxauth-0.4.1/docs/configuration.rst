
=============
Configuration
=============

This section contains information about how to configure your Django projects
to use *django-traxauth* and also contains a quick reference of the available
*settings* that can be used in order to customize the functionality of this
application.


Configuring your project
========================

In the Django project's ``settings`` module, add ``traxauth`` and all other
required apps to the ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = (
        ...
        'traxauth',
        'email_change',
        'registration',
        'profiles',
        'context_extras',
        'pagination',
        'recaptcha_works',
        'socialregistration',
        ...
    )

django-traxauth overrides some of the templates shipped with the ``admin`` app,
for example the templates for password reset. Therefore, the order in which the
apps appear in the ``INSTALLED_APPS`` list matters. In order to use the traxauth
templates, the ``admin`` app must appear after ``traxauth``::

    INSTALLED_APPS = (
        ...
        'traxauth',
        ...
        'admin',
        ...
    )


Update the project's URLs
=========================

*django-traxauth* requires that you update your project's URL patterns by
adding the application's own URL set. In your project's ``urls`` module
add the following patterns::

    urlpatterns = patterns('',
        ...
        # URLs for TraxAuth
        url('accounts/', include('traxauth.urls')),
        # URLs for django-email-change
        url('accounts/', include('email_change.urls')),
        # URLs for django-socialregistration
        url('accounts/external/', include('socialregistration.urls')),
    )

The URLs for the *django-email-change* have also been added.

The URLs for the *django-socialregistration* have also been added.

If the base URL component (*accounts*) is changed, also consider changing the
following Django settings:
    
    - ``LOGIN_REDIRECT_URL``    (By default: ``/accounts/profile/``)
    - ``LOGIN_URL``    (By default: ``/accounts/login/``)
    - ``LOGOUT_URL``    (By default: ``/accounts/logout/``)


Note about the available settings
=================================

*django-traxauth* uses several other applications in order to provide its full
functionality. Each of these applications has its own set of mandatory and
optional settings. Therefore, it is required to go through the list of settings
for each one of those application in order to properly configure your project
to use *django-traxauth*.


django-traxauth settings
========================

The following settings can be specified in the Django project's ``settings``
module to customize the functionality of *django-traxauth*.

There are both mandatory and optional settings.

Mandatory settings
------------------

``AUTH_PROFILE_MODULE``
    This should be set to point to ``traxauth.UserProfile`` model::
    
        AUTH_PROFILE_MODULE = 'traxauth.UserProfile'

Optional settings
-----------------

``TRAXAUTH_PROTECT_REGISTRATION_FORM``
    Boolean setting. Indicates whether the registration form should be protected
    by the reCaptcha field. Default is ``True``. Note that if this is set to
    ``False`` it is no longer required to set the reCaptcha keys.

``TRAXAUTH_PROTECT_PASSWORD_RESET_FORM``
    Boolean setting. Indicates whether the *lost password* form should be
    protected by the reCaptcha field. Default is ``True``. Note that if this is
    set to ``False`` it is no longer required to set the reCaptcha keys.

``TRAXAUTH_SITE_LOGO_URL``
    A URL to an image which is used as the logo.

``TRAXAUTH_ENABLE_GRAVATAR_SUPPORT``
    Boolean setting. By default, this is set to ``False``. If enabled, then
    gravatars are displayed.

``TRAXAUTH_SHOW_PROFILES_LIST``
    Boolean setting. By default the profile list is only displayed to
    authenticated users. If this is enabled, then the user list is made
    publicly available.

Example configuration::

    AUTH_PROFILE_MODULE = 'traxauth.UserProfile'
    TRAXAUTH_ENABLE_GRAVATAR_SUPPORT = True


django-email-change settings
============================

There are no mandatory settings for *django-email-change*. An example
configuration is::

    EMAIL_CHANGE_VERIFICATION_DAYS = 7

Also set the URLs as described previously::

    # URLs for django-email-change
    url('accounts/', include('email_change.urls')),


django-registration settings
============================

There are no mandatory settings for this application. Consult the
*django-registration* for more information on the options. An example that
can be used with *django-traxauth* is::

    ACCOUNT_ACTIVATION_DAYS = 7
    REGISTRATION_OPEN = True


django-recaptcha-works settings
===============================

Setting up the reCaptcha keys is mandatory only if any of the following traxauth
settings has been enabled:

- TRAXAUTH_PROTECT_REGISTRATION_FORM
- TRAXAUTH_PROTECT_PASSWORD_RESET_FORM

You can obtain a valid reCaptcha key pair for free from::

    http://www.google.com/recaptcha
    
Consult the *django-recaptcha-works* documentation for more information about
the settings. Below is an example configuration that can be used with
*django-traxauth*::

    RECAPTCHA_PUBLIC_KEY  = '...'
    RECAPTCHA_PRIVATE_KEY = '...'
    RECAPTCHA_USE_SSL = True
    RECAPTCHA_OPTIONS = {
        'theme': 'white',
        'lang': 'en',
        'tabindex': 0,
    }


django-context-extras settings
==============================

*django-traxauth* uses some of the context processors provided by
*django-context-extras*.

Django, by default, uses the following `context processors`__::

    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.debug',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'django.contrib.messages.context_processors.messages',
    )

__ http://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors

It is **mandatory** to add the following context processors to the above list
for proper *django-traxauth* operation::

    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        # Context processors provided by django-context-extras
        'context_extras.context_processors.current_site',
        'context_extras.context_processors.project_settings',
        ...
    )


django-pagination
=================

If your project does not override the default profile list as provided by
django-traxauth, then it is **mandatory** to set the following middleware class
provided by *django-pagination*::

    MIDDLEWARE_CLASSES = (
        ...
        # django-pagination middleware class
        'pagination.middleware.PaginationMiddleware',
        ...
    )


django-socialregistration
=========================

Set URLs as it was described previously::

    # URLs for django-socialregistration
    url('accounts/external/', include('socialregistration.urls')),
        
Twitter
- http://dev.twitter.com/apps/new




Synchronize the project database
================================

Finally, synchronize the project's database using the following command::

    python manage.py syncdb


Media files
===========

*django-traxauth* ships with some media files. In order to use the provided
media files you have to copy the directory structure under ``traxauth/media/``
to your project's ``MEDIA_ROOT``.

Alternatively, you can use django-staticfiles_ to do this in one step. Actually,
this is the preferred::

    python manage.py build_static -l --noinput

.. _django-staticfiles: http://bitbucket.org/jezdez/django-staticfiles

Also make sure the ``MEDIA_ROOT/TRAXAUTH_AVATAR_ROOT`` directory is writable by
the web server process.

