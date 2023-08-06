====================
Django Activity Sync
====================

Django-activitysync is an easy to use social activity aggregator for Django
projects.

It can be used to store and display activity from a range of social networks
(such as Twitter, Reddit, Google Reader, etc). Unlike other utilities for
accessing and displaying activity, django-activitysync separates rendering
from activity updating. All activity information is stored in the project's
database using Django models, providing great performance for page requests.
Updating activities happens through a Django management command, which can
be automated by using a utility like cron.


--------
Features
--------

- Currently supports the following activity providers:

    * `Twitter`_
    * `Google Reader`_
    * `Reddit`_

- Providers are implemented using a simple, common interface, making it very
  easy to add support for additional networks


------------
Dependencies
------------
Dependencies that *must* be meet to use the application:

- Twitter support depends on python-twitter_

- Google Reader and Reddit support depend on feedparser_


------------
Installation
------------

From pypi_::

    $ pip install django-activitysync

or::

    $ easy_install django-activitysync

or clone from Bitbucket_::

    $ hg clone https://bitbucket.org/dancarroll/django-activitysync

and add social_auth to PYTHONPATH::

    $ export PYTHONPATH=$PYTHONPATH:$(pwd)/django-activitysync/

or::

    $ cd django-activitysync
    $ sudo python setup.py install


-------------
Configuration
-------------
- Add activitysync to PYTHONPATH and installed applications::

    INSTALLED_APPS = (
        ...
        'activitysync'
    )

- Add desired providers to ACTIVITYSYNC_PROVIDERS setting::

    ACTIVITYSYNC_PROVIDERS = (
        'activitysync.providers.googlereader.GoogleReaderProvider',
        'activitysync.providers.twitterprovider.TwitterProvider',
        'activitysync.providers.redditprovider.RedditProvider',
    )

- Setup provider settings (dependent on which providers are added). Settings
  required for built-in providers are::

    TWITTER_USERNAME        = ''
    REDDIT_USERNAME         = ''
    GOOGLEREADER_SHARED_RSS = '' # URL of your shared items RSS
    GOOGLEREADER_PUBLIC_URL = '' # URL to public page

- Sync database to create needed models::

    ./manage syncdb

  or (if you have South installed)::

    ./manage migrate activitysync


.. _Twitter: http://twitter.com/
.. _Google Reader: http://www.google.com/reader/
.. _Reddit: http://reddit.com/
.. _pypi: http://pypi.python.org/pypi/django-activitysync/
.. _Bitbucket: https://bitbucket.org/dancarroll/django-activitysync
.. _python-twitter: http://code.google.com/p/python-twitter/
.. _feedparser: http://www.feedparser.org/

