.. _deprecated_plugins:

Deprecated :mod:`repoze.who` Plugins
====================================

.. note::
    The following plugins were originally distributed with :mod:`repoze.who`,
    but are now deprecated.  The developers discourage their use except as
    needed to migrate a system deployed using them under :mod:`repoze.who`
    1.0 to the newer usage patterns of :mod:`repoze.who` 2.0.

.. module:: repoze.who.plugins.cookie

.. class:: InsecureCookiePlugin(cookie_name)

  A :class:`InsecureCookiePlugin` is an ``IIdentifier`` plugin.  It
  stores identification information in an insecure form (the base64
  value of the username and password separated by a colon) in a
  client-side cookie.  It accepts a single required argument named
  *cookie_name*.  This is the cookie name of the cookie used to store
  the identification information.  The plugin also accepts two optional
  arguments:  *cookie_path* is the URL path root which scopes the cookie,
  and *charset* is the name of a codec used to convert the login and password
  to and from unicode.

.. module:: repoze.who.plugins.form

.. class:: FormPlugin(login_form_qs, rememberer_name [, formbody=None [, formcallable=None]])

  A :class:`FormPlugin` is both an ``IIdentifier`` and ``IChallenger``
  plugin.  It intercepts form POSTs to gather identification at
  ingress and conditionally displays a login form at egress if
  challenge is required.  *login_form_qs* is a query string name used
  to denote that a form POST is destined for the form plugin (anything
  unique is fine), *rememberer_name* is the "configuration name" of
  another ``IIdentifier`` plugin that will be used to perform
  ``remember`` and ``forget`` duties for the FormPlugin (it does not
  do these itself).  For example, if you have a cookie identification
  plugin named ``cookie`` defined in your middleware configuration,
  you might set *rememberer_name* to ``cookie``.  *formbody* is a
  literal string that should be displayed as the form body.
  *formcallable* is a callable that will return a form body if
  *formbody* is None.  If both *formbody* and *formcallable* are None,
  a default form is used.

.. class:: RedirectingFormPlugin(login_form_url, login_handler_path, logout_handler_path, rememberer_name)

  A :class:`RedirectingFormPlugin` is both an ``IIdentifier`` and
  ``IChallenger`` plugin.  It intercepts form POSTs to gather
  identification at ingress and conditionally redirects a login form
  at egress if challenge is required (as opposed to the
  :class:`FormPlugin`, it does not handle its own form generation).
  *login_form_url* is a URL that should be redirected to when a
  challenge is required.  *login_handler_path* is the path that the
  form will POST to, signifying that the plugin should gather
  credentials.  *logout_handler_path* is a path that can be called to
  log the current user out when visited. *rememberer_name* is the
  configuration name of another ``IIdentifier`` plugin that will be
  used to perform ``remember`` and ``forget`` duties for the
  RedirectingFormPlugin (it does not do these itself).  For example,
  if you have a cookie identification plugin named ``cookie`` defined
  in your middleware configuration, you might set *rememberer_name* to
  ``cookie``.
