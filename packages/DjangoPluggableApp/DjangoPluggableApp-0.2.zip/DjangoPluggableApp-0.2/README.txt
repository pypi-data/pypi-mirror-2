DjangoPluggableApp is a package to allow:

- django users to install and configure third-party django applications

- developpers to create an distribute django apps.

DjangoPluggableApp is **not** intrusive. This mean that:

- end users can use applications without a DjangoPluggableApp entry_point in
  their projects

- an application based on the provided template can be used by end users
  without DjangoPluggableApp installed.

Installation
============

With easy_install::

  $ easy_install -U DjangoPluggableApp

With pip::

  $ pip install DjangoPluggableApp
