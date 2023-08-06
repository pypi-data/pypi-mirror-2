
=====
Usage
=====

This section contains information, including examples, about how to use
*django-middleware-extras* in your existing Django projects or applications.


django-middleware-extras Help
========================================================================
This file contains detailed information on how to configure and use
``django-middleware-extras``.


Middleware
==========
In order to use the provided middleware it is required that you add
them to the list of the middleware classes your project uses.

Django, by default, uses the following `middleware classes`__::

    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
    )

__ http://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes

The middleware classes provided by ``django-context-extras`` are:

1. ReverseProxyHttpsHeadersMiddleware
-------------------------------------
By default, Django determines whether the web server communicates with the
clients over the HTTP or HTTPS protocol by checking the value of the ``HTTPS``
environment variable. If this variable is set to ``on``, then Django's
``request.is_secure()`` method returns ``True``. This works well, except for
those cases that the web server (*Reverse Proxy*), that sits between the Django
application server and the web, communicates with the Django application server
using the HTTP protocol. In this case, it is impossible for the reverse
proxy to "transmit" the ``HTTPS`` environment variable to the Django application
server. So, the only way the reverse proxy can notify the Django application
server about the protocol (HTTP or HTTPS) it uses to communicate with the
clients is by sending specific HTTP headers.

By convention several HTTP headers, such as ``X-Forwarded-Protocol``,
``X-Forwarded-Ssl``, ``Front-End-Https``, are often used for this purpose. The
problem in this case is that malicious clients can send such headers without
actually communicating with the reverse proxy over a secure connection.
Reverse proxies usually do not filter such headers, so the headers finally make
it to the Django application server. Therefore, if security matters, such
headers should not be trusted by the application server.

Django-context-extras provides the administrator with the ability to define
which headers the application server should trust in order to determine whether
the reverse proxy communicates with the clients over the HTTPS protocol. At
the same time, the reverse proxy should be configured to send these headers
to the application server if it actually communicates with the clients over
HTTPS. It is extremely hard for malicious clients to guess which headers are
used for the reverse_proxy <-> app_server communication, so this method is
very secure and effective at the same time.

In order to implement this functionality, you have to do the following
3 things:

1. Add ``REVERSE_PROXY_HTTPS_HEADERS`` in your project's ``settings.py`` file
   and add the header_name/header_value pairs that your Django project should
   trust so as ``request.is_secure()`` to return *True*. For instance::

       REVERSE_PROXY_HTTPS_HEADERS = (
           ('x-forwarded-ssl', 'on'),
       )

   Note that **all** these headers must match those the reverse proxy sends.

2. Add the ``ReverseProxyHttpsHeadersMiddleware`` in the list of your project's
   middleware classes::

       MIDDLEWARE_CLASSES = (
           ...
           'middleware_extras.middleware.ReverseProxyHttpsHeadersMiddleware',
       )

3. Configure your reverse proxy to send the headers, which you have specified
   in the REVERSE_PROXY_HTTPS_HEADERS setting, to the Django application server,
   whenever communication with the clients is done over the HTTPS protocol.
   Configuring the reverse proxy is out of the scope of this document, so
   consult the web server's documentation on how to do this.


2. SSLRequireMiddleware
-----------------------

TODO

