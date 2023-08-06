
============
Introduction
============

This section contains an introduction to *django-context-extras*, including general
information about how to submit bug reports and make feature requests.

django-context-extras provides some extra context processors that are often needed by Django projects.

Licensed under the *Apache License version 2.0*. More licensing information
exists in the license_ section.


Features
========

This application currently provides two extra context processors:

*current_site*
    Adds the current ``site`` instance to the template context.
*project_settings*
    Adds the project's ``settings`` object to the template context, so you can
    access the project settings from within the templates.
*protocol_host*
    Adds the ``PROTOHOST`` variable to the template context. The variable contains
    the complete URL to the host, for example: ``http://example.org:8080``

Documentation
=============

Apart from the `django-context-extras Online Documentation`_, more information about the
installation, configuration and usage of this application may be available
at the project's wiki_.

.. _`django-context-extras Online Documentation`: http://packages.python.org/django-context-extras
.. _wiki: http://www.codetrax.org/projects/django-context-extras/wiki


Donations
=========

This software is released as free-software and provided to you at no cost. However,
a significant amount of time and effort has gone into developing this software
and writing this documentation. So, the production of this software has not
been free from cost. It is highly recommended that, if you use this software
*in production*, you should consider making a donation.

To make a donation, please visit the CodeTRAX `donations page`_ which contains
a PayPal_ *donate* button.

Thank you for considering making a donation to django-context-extras.

.. _`donations page`: https://source.codetrax.org/donate.html
.. _PayPal: https://www.paypal.com


Bugs and feature requests
=========================

In case you run into any problems while using this application or think that
a new feature should be implemented, it is highly recommended you submit_ a new
report about it at the project's `issue tracker`_.

Using the *issue tracker* is the recommended way to notify the authors about
bugs or make feature requests. Also, before submitting a new report, please
make sure you have read the `new issue guidelines`_.

.. _submit: http://www.codetrax.org/projects/django-context-extras/issues/new
.. _`issue tracker`: http://www.codetrax.org/projects/django-context-extras/issues
.. _`new issue guidelines`: http://www.codetrax.org/NewIssueGuidelines


Support
=======

CodeTRAX does not provide support for django-context-extras.

You can still get community support at the `Community Support Forums`_:

.. _`Community Support Forums`: http://www.codetrax.org/projects/django-context-extras/boards


License
=======

Copyright 2010 George Notaras <gnot [at] g-loaded.eu>

Licensed under the *Apache License, Version 2.0* (the "*License*");
you may not use this file except in compliance with the License.

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

A copy of the License exists in the product distribution; the *LICENSE* file.
For copyright and other important notes regarding this release please read
the *NOTICE* file.
