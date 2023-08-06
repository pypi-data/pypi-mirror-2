
=====
Usage
=====

This section contains information, including examples, about how to use
*django-context-extras* in your existing Django projects or applications.


Context Processors
==================
In order to use the provided context processors it is required that you add
them to the list of the context processors your project uses.

Django, by default, uses the following `context processors`__::

    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.debug',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'django.contrib.messages.context_processors.messages',
    )

__ http://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors

The context processors provided by ``django-context-extras`` are:


*current_site* context processor
--------------------------------

Adds the current **site** object to the template context.

To add the *current_site* context processor to your project, add the
``context_extras.context_processors.current_site`` module in the
``TEMPLATE_CONTEXT_PROCESSORS`` setting in your ``settings.py`` file::

    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        'context_extras.context_processors.current_site',
        ...
    )


*project_settings* context processor
------------------------------------

Adds the project's **settings** object to the template context.

To add the *project_settings* context processor to your project, add the
``context_extras.context_processors.project_settings`` module in the
``TEMPLATE_CONTEXT_PROCESSORS`` setting in your ``settings.py`` file::

    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        'context_extras.context_processors.project_settings',
        ...
    )


*protocol_host* context processor
---------------------------------

Adds the ``PROTOHOST`` variable to the template context. The variable contains
the complete URL to the host, for example: ``http://example.org:8080``

To add the *protocol_host* context processor to your project, add the
``context_extras.context_processors.protocol_host`` module in the
``TEMPLATE_CONTEXT_PROCESSORS`` setting in your ``settings.py`` file::

    TEMPLATE_CONTEXT_PROCESSORS = (
        ...
        'context_extras.context_processors.protocol_host',
        ...
    )

