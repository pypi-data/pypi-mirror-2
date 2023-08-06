.. contents::

================
yaco.recipe.cert
================

Buildout recipe that creates self signed certificates, useful for adding SSL support to your
development deployment.

It needs the openssl binary installed in your system.

Tests need to be written.

Use at your own risk and specially, use real certificates in production.

Usage
=====

Example usage::

  [buildout]
  parts = mycert

  [mycert]
  recipe = yaco.recipe.cert
  hostname = test.example.com
  country = US
  city = Springfield
  organization = Example Corp.
  locality = Springfield

After running buildout you will have your self signed certificate in the parts directory.
