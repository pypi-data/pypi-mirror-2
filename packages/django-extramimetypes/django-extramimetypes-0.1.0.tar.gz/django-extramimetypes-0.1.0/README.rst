django-extramimetypes
=====================

A Django app that hooks Python's ``mimetypes`` module to allow extra
mimetype guesses to be added via a project's ``settings.py``.

I wrote it because on Mac OSX, Django's static serve view doesn't correctly set
the ``Content-Type`` header for ``.htc`` files. This means that CSS behaviours
for IE won't work! The view makes use of Python's ``mimetypes.guess_type``
function, and so this app solves the problem in a generalised way.


Usage
-----

Define a ``MIMETYPES`` setting in your project that maps extensions to types,
e.g.::

    MIMETYPES = {
        ".htc": "text/x-component",
    }

And then to use it::

    >>> import mimetypes
    >>> mimetypes.guess_type("test.htc")
    ("text/x-component", None)

In order for the mimetypes defined in ``settings.py`` to be added,
``extramimetypes`` must be imported. If you're using any of Django's database
machinery (highly likely) this will happen automatically.

However under some special circumstances (e.g. testing this app) you'll need to
import it explicitly. A good place to do this is your ``urls.py``.


Installation
------------

1. Download and install: ``pip install django-extramimetypes``
2. Add ``"extramimetypes"`` to the ``INSTALLED_APPS`` setting in your project.
