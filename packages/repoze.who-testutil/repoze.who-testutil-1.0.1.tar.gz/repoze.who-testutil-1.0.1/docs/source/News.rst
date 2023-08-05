********************************
**repoze.who-testutil** releases
********************************

This document describes the releases of :mod:`repoze.who-testutil`.


**repoze.who-testutil** 1.0.1 (2010-08-17)
=============================================

* Made sure repoze.who 1 is installed, not v2.
* Fixed typo in a code example in the documentation, reported by Ryan McKillen.


.. _1.0:

**repoze.who-testutil** 1.0 (2010-02-22)
=============================================

* Fixed typo in a code sample of the home page.
* Explained how to use it with :mod:`repoze.what`.
* Fixed a bug related to the Content-Length, thanks to Ian Bicking and
  Christopher Perkins.


.. _1.0rc1:

**repoze.who-testutil** 1.0rc1 (2009-03-08)
===========================================
* :class:`repoze.who.plugins.testutil.AuthenticationForgerPlugin` ignored the
  original response headers on challenge.


.. _1.0b2:

**repoze.who-testutil** 1.0b2 (2009-03-02)
==========================================

* Specified the required version of :mod:`repoze.who`, otherwise the buggy
  setuptools won't install it.


.. _1.0b1:

**repoze.who-testutil** 1.0b1 (2009-02-27)
==========================================

This is the first release of **repoze.who-testutil**, which ships the following
components:

* :class:`repoze.who.plugins.testutil.AuthenticationForgerPlugin`, a
  :mod:`repoze.who` plugin which acts as identifier, authenticator and
  challenger.
* :class:`repoze.who.plugins.testutil.AuthenticationForgerMiddleware`, a
  proxy to :class:`repoze.who.middleware.PluggableAuthenticationMiddleware`
  to forge authentication easily.
* :func:`repoze.who.plugins.testutil.make_middleware`.
* :func:`repoze.who.plugins.testutil.make_middleware_with_config`.
