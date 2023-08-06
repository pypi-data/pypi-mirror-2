The personal bar is hidden for anonymous users
==============================================

This package was created for the usecase that we have a Plone site where is
no user interaction. So we don't need a login possibility for all users,
provided with the personal bar. But if someone is logged in it's very usefull
to have the personal bar. So the personal bar is hidden to anonymous users, but
show to authenticated ones.

Tested with Plone 4.0.4.


    >>> from os.path import dirname, join
    >>> from plone.app.testing import (
    ...     TEST_USER_NAME,
    ...     TEST_USER_PASSWORD,
    ... )
    >>> from plone.testing.z2 import Browser
    >>> browser = Browser(layer['app'])
    >>> browser.handleErrors = False
    >>> portal = layer['portal']


As an anonymous user we can't see the personal bar::

    >>> browser.open(portal.absolute_url())
    >>> '<a href="http://nohost/plone/@@personal-preferences">' in browser.contents
    False
    >>> '<a href="http://nohost/plone/dashboard">' in browser.contents
    False


But after a login, it's there::

    >>> browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))
    >>> browser.open(portal.absolute_url())
    >>> '<a href="http://nohost/plone/@@personal-preferences">' in browser.contents
    True
    >>> '<a href="http://nohost/plone/dashboard">' in browser.contents
    True
