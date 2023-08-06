Django URL internationalization
===============================

This Django app makes it possible to prefix URL patterns with the active
language and to make URL patterns translatable by using gettext. As well this
package contains a patch for the ``LocaleMiddleware`` so it is able to activate
the right language (based on the language-prefix in the requested URL).

.. note::

    During the DjangoCon EU 2011 sprints, I wrote a patch for including this
    functionality into the Django core. This patch was accepted and will be
    included in Django 1.4 (thanks to Jannis Leidel and Russell Keith-Magee for
    their feedback and reviewing the patch).
    
    
    In the 0.6 version of this package, I rewrote the API so that it will match
    with the upcoming Django 1.4 version. You can read more about this in the
    `Django documentation (dev) <http://docs.djangoproject.com/en/dev/topics/i18n/internationalization/#specifying-translation-strings-in-url-patterns>`_.


Translating URL patterns
------------------------

After installing this package, URL patterns can also be marked translatable
using the ``ugettext_lazy()`` function. Example::

    from django.conf.urls.defaults import patterns, include, url
    from django.conf.urls.i18n import i18n_patterns
    from django.utils.translation import ugettext_lazy as _

    urlpatterns = patterns(''
        url(r'^sitemap\.xml$', 'sitemap.view', name='sitemap_xml'),
    )

    news_patterns = patterns(''
        url(r'^$', 'news.views.index', name='index'),
        url(_(r'^category/(?P<slug>[\w-]+)/$'), 'news.views.category', name='category'),
        url(r'^(?P<slug>[\w-]+)/$', 'news.views.details', name='detail'),
    )

    urlpatterns += i18n_patterns('',
        url(_(r'^about/$'), 'about.view', name='about'),
        url(_(r'^news/$'), include(news_patterns, namespace='news')),
    )


After you've created the translations, the ``reverse()`` function will return
the URL in the active language. Example::

    from django.core.urlresolvers import reverse
    from django.utils.translation import activate

    >>> activate('en')
    >>> reverse('news:category', kwargs={'slug': 'recent'})
    '/en/news/category/recent/'

    >>> activate('nl')
    >>> reverse('news:category', kwargs={'slug': 'recent'})
    '/nl/nieuws/categorie/recent/'


Installation
------------

* Install the ``django-i18nurls`` package (eg: ``pip install django-i18nurls``).

* Add ``i18nurls`` to your ``settings.INSTALLED_APPS``.

* Add ``django.middleware.locale.LocaleMiddleware`` to your ``settings.MIDDLEWARE_CLASSES``
  (if it is not already there, make sure it comes before the ``CommonMiddleware``).


Changelog
---------

v0.6.1
~~~~~~

* templates and locale folder added to setup.py script (Issue #1).

v0.6
~~~~

* API changed so it will match with ``i18n_patterns`` in upcoming Django 1.4 release.

v0.5.2
~~~~~~

* Some README errors corrected.

v0.5.1
~~~~~~

* Some code cleanup.

v0.5
~~~~

* Initial release.
