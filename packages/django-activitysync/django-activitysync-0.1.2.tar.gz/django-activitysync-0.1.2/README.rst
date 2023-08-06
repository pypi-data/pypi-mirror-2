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


Features
========

- Currently supports the following activity providers:

    * `Twitter`_
    * `Google Reader`_
    * `Reddit`_

- Providers are implemented using a simple, common interface, making it very
  easy to add support for additional networks


Dependencies
============

Dependencies that *must* be meet to use the application:

- Twitter support depends on python-twitter_

- Google Reader and Reddit support depend on feedparser_


Installation
============

From pypi_::

    $ pip install django-activitysync

or::

    $ easy_install django-activitysync

or clone from Bitbucket_::

    $ hg clone https://bitbucket.org/dancarroll/django-activitysync

and add activitysync to PYTHONPATH::

    $ export PYTHONPATH=$PYTHONPATH:$(pwd)/django-activitysync/

or::

    $ cd django-activitysync
    $ sudo python setup.py install


Configuration
=============

- Add activitysync to ``INSTALLED_APPS`` in settings.py::

    INSTALLED_APPS = (
        ...
        'activitysync'
    )

- Add desired providers to ``ACTIVITYSYNC_PROVIDERS`` setting::

    ACTIVITYSYNC_PROVIDERS = (
        'activitysync.providers.googlereader.GoogleReaderProvider',
        'activitysync.providers.twitterprovider.TwitterProvider',
        'activitysync.providers.redditprovider.RedditProvider',
    )

- Add provider settings to settings.py (dependent on which providers are added).
  Settings required for built-in providers are::

    TWITTER_USERNAME        = ''
    REDDIT_USERNAME         = ''
    GOOGLEREADER_SHARED_RSS = '' # URL of your shared items RSS
    GOOGLEREADER_PUBLIC_URL = '' # URL to public page

- Sync database to create needed models::

    python manage.py syncdb

  or (if you have South installed)::

    python manage.py migrate activitysync


Usage
=====

Fetching and creating activity items
------------------------------------

Once configuration is completed, run the included management command
to fetch activities for the configured providers::

    python manage.py updateactivities

The command will print out all new activities to the command line. All
activity items are stored with a unique guid value, so this command can
be run as often as needed without worrying about creating duplicate values.
In a production site, this command likely would be added to the crontab (or
other scheduler) to run fairly often (such as every 30 minutes).

There are a few options available for the management command.

- Use the ``--send-result`` option to send an email to the site admins
  (controlled by the Django ADMIN setting) with the newly added activities
  (no email is sent if there are no new items)::

    python manage.py updateactivities --send_result

- Use the ``--dry-run option`` to output the items to the console, but not
  actually create items in the database::

    python manage.py updateactivities --dry-run


Using activity items
--------------------

Activity items can be accessed like any other model using Django's ORM. Here
is a quick example of getting all published activity items (fetched items
default to public, but can be hidden by modifying the item in the Django
admin site)::

    from django.shortcuts import render_to_response
    from activitysync.models import Activity

    def index(request):
        return render_to_response(
            'index.html',
            { 'activities': Activity.objects.published() }
        )

Django-activitysync also provides a template tag for displaying items::

    {% load activitysync_extras %}
    {% render_activities activities %}

The ``render_activities`` template tag will pass the object list and
``MEDIA_URL`` values to the template ``activitysync/activities_tag.html``.
The project comes with a sample template that will be used by default, or you
can use it as a basis for your own. A second template tag,
``render_activities_with_date_headers`` renders the activity list along with
date headers for each unique day encountered.


.. _Twitter: http://twitter.com/
.. _Google Reader: http://www.google.com/reader/
.. _Reddit: http://reddit.com/
.. _pypi: http://pypi.python.org/pypi/django-activitysync/
.. _Bitbucket: https://bitbucket.org/dancarroll/django-activitysync
.. _python-twitter: http://code.google.com/p/python-twitter/
.. _feedparser: http://www.feedparser.org/

