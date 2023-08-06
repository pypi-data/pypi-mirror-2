.. -*- restructuredtext -*-

django-articles is the blog engine that I use on codekoala.com

Features
========

* Tags for articles, with a tag cloud template tag
* Auto-completion for tags in the Django admin
* Ability to post in the future
* Article expiration facilities
* Articles from email
* Article attachments
* Article statuses--"draft" and "finished" are there by default
* Allows articles to be written in plain text/HTML or using Markdown,
  ReStructured Text, or Textile markup
* Related articles
* Follow-up articles
* Comments by Disqus
* Article archive, with pagination
* Internationalization-ready
* Detects links in articles and creates a per-article index for you
* Word count
* RSS feeds for the latest articles
* RSS feeds for the latest articles by tag

Requirements
============

``django-articles`` wants a modern version of Django--something after 1.1.  It
used to rely on ``django.contrib.comments`` for commenting needs, but I
recently switched to `Disqus <http://www.disqus.com/>`_.  Included herein is a
management command to convert ``django.contrib.comments`` comments to Disqus.

This project also expects ``django.contrib.sites``, ``django.contrib.admin``,
``django.contrib.markup``, ``django.contrib.auth``,
``django.contrib.humanize``, and ``django.contrib.syndication`` to be properly
installed.

Installation
============

Download ``django-articles`` using *one* of the following methods:

Checkout from Mercurial
-----------------------

Use one of the following commands::

    hg clone http://django-articles.googlecode.com/hg/ django-articles
    hg clone http://bitbucket.org/codekoala/django-articles/

The CheeseShop
--------------

Use one of the following commands::

    pip install django-articles
    easy_install django-articles

Configuration
=============

First of all, you must add this project to your list of ``INSTALLED_APPS`` in
``settings.py``::

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.humanize',
        'django.contrib.markup',
        'django.contrib.sessions',
        'django.contrib.sites',
        'django.contrib.syndication',
        ... 
        'articles',
        ...
    )

Run ``manage.py syncdb``.  This creates a few tables in your database that are
necessary for operation.

Next, set a couple of settings in your ``settings.py``:

* ``DISQUS_USER_API_KEY``: Your user API key from Disqus.  This is free, and
  you can learn how to get it from  `Disqus's API Page <http://2ze.us/ME>`_ or
  you can try http://disqus.com/api/get_my_key/ when you're logged into Disqus.
  You only need this one if you're going to be converting comments from
  ``django.contrib.comments`` to Disqus.
* ``DISQUS_FORUM_SHORTNAME``: The name of your Disqus site.  This is what's
  used to link comments to your site.

Also, make sure that you have the following context processors in your
``TEMPLATE_CONTEXT_PROCESSORS`` tuple:

* ``django.contrib.auth.context_processors.auth``
* ``django.core.context_processors.i18n``
* ``django.core.context_processors.media``
* ``django.core.context_processors.request``

Template Integration
====================

There are several template blocks that ``django-articles`` expects your
``base.html`` file to contain:

* ``title``
* ``meta-keywords``
* ``meta-description``
* ``extra-head``
* ``content``
* ``footer``

Tag Auto-Completion
===================

If you would like to take advantage of the auto-completion feature for tags,
copy the files from the ``articles/media`` directories into your static media
directory.  ``django-articles`` expects to find each of those directories/files
in your ``settings.MEDIA_URL`` directory--if this does not suit your needs, you
may override the ``Media`` class of ``articles.forms.ArticleAdminForm`` with
the appropriate paths.

Another assumption that is made by this feature is that the prefix you assign
to your ``django-articles`` installation in your ``ROOT_URLCONF`` will be
``^blog/``.  For example::

    url(r'^blog', include('articles.urls')),

If this does not match your installation, all you need to change is the
``js/tag_autocomplete.js`` to reflect the proper path.

When that's done, you should be able to begin using ``django-articles``!

Articles From Email
===================

.. admonition:: Added In 1.9.2

    The articles from email feature was added in version **1.9.2**.  It
    requires Python 2.4 or greater.

I've been working on making it possible for ``django-articles`` to post
articles that you email to a special mailbox.  This seems to be working on the
most basic levels right now.  It's not been tested in very many scenarios, and
I would appreciate it if you could post problems with it in the ticket tracker
at http://bitbucket.org/codekoala/django-articles/ so we can make it work
really well.

Things to keep in mind:

* Any **active** user who is a ``django.contrib.auth.models.User`` and has an
  email address associated with their user information is a valid sender for
  articles from email.  This is how the author of an article is determined.
* Only the following fields are currently populated by the articles from email
  feature:

    * author
    * title
    * slug (uniqueness is handled)
    * content
    * markup
    * publish_date
    * is_active

  Any and all other attributes about an article must be configured later on
  using the standard mechanisms (aka the Django admin).
* There is a new management command to handle all of the magic for this
  feature: ``check_for_articles_from_email``.  This command is intended to be
  called either manually or via external scheduling utilities (like ``cron``)
* Email messages **are deleted** after they are turned into articles.  This
  means that you should probably have a *special mailbox dedicated to
  django-articles and articles from email*.  However, only emails whose sender
  matches the email address of an active user are deleted (as described above).
* Attachments are currently not bothered with.  Don't worry, they will be in
  the future. :D

Configuration
-------------

There are several new variables that you can configure in your ``settings.py``
to enable articles from email, specifying a ``ARTICLES_FROM_EMAIL`` dictionary:

* ``protocol`` - Either ``IMAP4`` or ``POP3``.  *Default*: ``IMAP4``
* ``host`` - The mail server. *Example*: ``mail.yourserver.com``
* ``port`` - The port to use to connect to your mail server
* ``keyfile`` - The keyfile used to access your mail server.  This is only used
  if ``ssl`` is ``True``, and even then it's optional. *untested*
* ``certfile`` - The certfile used to access your mail server.  This is only
  used if ``ssl`` is ``True``, and even then it's optional. *untested*
* ``user`` - The username used to access your mailbox
* ``password`` - The password associated with the user to access your mailbox
* ``ssl`` - Whether or not to connect to the mail server using SSL.  *Default*:
  ``False``
* ``autopost`` - Whether or not to automatically post articles that are created
  from email messages.  If this is ``False``, the articles will be marked as
  inactive and you must manually make them active. *Default*: ``False``
* ``markup`` - The default markup language to use for articles from email.
  Options include:

    * ``h`` for HTML/plain text
    * ``m`` for Markdown
    * ``r`` for reStructuredText
    * ``t`` for Textile

  *Default*: ``h``
* ``acknowledge`` - Whether or not to email out an acknowledgment
  message when articles are created from email.  *Default*: ``False``

Example configuration::

    ARTICLES_FROM_EMAIL = {
        'protocol': 'IMAP4',
        'host': 'mail.yourserver.com',
        'port': 9000,
        'keyfile': '/path/to/keyfile',
        'certfile': '/path/to/certfile',
        'user': 'your_username',
        'password': 'your_password',
        'ssl': True,
        'autopost': True,
        'markup': 'r',
        'acknowledge': True,
    }

Article Attachments
===================

You can now attach files to your articles and have them be included with the
article on the site.  Attachments can be created using the Django admin while
composing your articles.  You may also attach files to emails that you send to
the special mailbox (described above) if you so desire.

Article Statuses
================

As of ``1.9.6``, you may specify the state of an article when you save it.
This allows you to begin composing an article, save it, and come back later to
finish it.  In the past, this behavior was handled by not setting a publish
date for the article.  However, saving an unfinished article with a non-live
status allows superusers to view the article on the site as though it were
live.  In the future, I plan to allow authors to view non-live versions of
their articles.

The default status for an article will always be the Article Status object with
the lowest ``ordering`` value.  This includes negative integers.  If you want
all articles to be ``Finished`` by default, go ahead and update the
``ordering`` on that object to be less than the ``ordering`` value for the
``Draft`` object (and/or any others you create).

Good luck!  Please contact me with any questions or concerns you have with the
project!

