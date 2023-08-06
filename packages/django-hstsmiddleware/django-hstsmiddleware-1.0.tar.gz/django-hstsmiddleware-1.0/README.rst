django-hstsmiddleware
=====================

Forces the use of `HTTPS` using `HTTP Strict Transport Security`
(HSTS).


Installation and Usage
----------------------

Install the package, add ``django_hstsmiddleware`` to
``settings.INSTALLED_APPS``, and add
``django_hstsmiddleware.middleware.HSTSMiddleware`` to the top of
``settings.MIDDLEWARE_CLASSES``.

The following Django settings control its default behaviour:

``settings.HSTS_REDIRECT_TO``:
    Specifies the URI to redirect a User Agent to, if it tries
    to use a non-secure connection. Responds with HTTP Moved
    Permanently.

    Defaults to ``None``, so no redirect occurs. Instead, responds
    with HTTP Bad Request.

``settings.HSTS_MAX_AGE``:
    The maximum number of seconds that a User Agent will remember
    that this server must be contacted over HTTPS.

    Defaults to ``31536000``, or approximately one year.

``settings.HSTS_INCLUDE_SUBDOMAINS``:
    If true, tells a User Agent that all subdomains must also be
    contacted over HTTPS, in addition to the current domain.

    Defaults to ``False``
