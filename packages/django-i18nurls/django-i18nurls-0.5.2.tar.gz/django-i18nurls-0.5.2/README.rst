Django URL internationalization
===============================

This Django pluggable makes it possible to translate URL patterns by using gettext.
As well it contains a custom patterns function for prefixing URLs with the active
language-code (eg: ``/en/news/``, ``/nl/nieuws/``) and a middleware to activate
the language code in the prefix (for incoming request).


Examples
--------

::
    
    # urls.py
    from django.conf.urls.defaults import patterns, include, url
    from django.utils.translation import ugettext_lazy as _

    from i18nurls.defaults import language_prefixed_patterns
    
    
    patterns = language_prefixed_patterns('',
        url(_(r'^users/register/$'), 'your.view', name='account-register'),
    )
    
    # In your shell, after updating your translations (with makemessages / compilemessages)
    >>> activate('nl')
    >>> reverse('account-register')
    '/nl/gebruikers/registeren/'
    
    >>> activate('en')
    >>> reverse('account-register')
    '/en/users/register/'


Installation
------------

* Install the ``django-i18nurls`` package (eg: ``pip install django-i18nurls``).

* Add ``i18nurls`` to your ``settings.INSTALLED_APPS``.

* Add ``i18nurls.middleware.LocaleMiddleware`` to your ``settings.MIDDLEWARE_CLASSES``.
  Note: This middleware replaces the default Django LocaleMiddleware.
