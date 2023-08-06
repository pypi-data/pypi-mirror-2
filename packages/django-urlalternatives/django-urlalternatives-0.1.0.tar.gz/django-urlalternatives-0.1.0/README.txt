==========================================================================
 django-urlalternatives - Alternative Django views under same URL pattern
==========================================================================

Django URL alternatives provides a way for dispatching one URL pattern to the
first alternative view (callback function) in a list that returns success.

:version: 0.1 (or corresponding Mercurial revision hash)
:web: http://gw.tnode.com/0483-Django/
:author: GW <gw.2011@tnode.com or http://gw.tnode.com/>
:license: GPLv3+
:keywords: url alternatives, dispatcher, views, django, urlconf, same pattern

Description
===========

In case you want to assing in an URLconf the same URL pattern to more than one
view (or callback function), such that the next ones are fallbacks in case of
errors (ie. HTTP response codes >= 400). This is often the case when combining
different apps with dynamic URLs (such as CMSs) and you want to respond with the
one that has that content.

Usage
=====

As you can see from the following example the URL alternatives dispatcher is
simply used as part of the ``urlpatterns`` variable in ``urls.py`` and supports
passing of positional and keyword arguments, eg.:

    urlpatterns += pattern('',
        (r'^', 'urlalternatives.views.dispatcher', {'callbacks':[
            app1.views.failing404,
            'app2.views.working',
            (redirect_to, [], {'url':'/'}),
         ]}),
     )

