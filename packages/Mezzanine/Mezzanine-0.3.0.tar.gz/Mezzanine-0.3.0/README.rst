--------
Overview
--------

Mezzanine is a content management platform built using the `Django`_ framework. It is BSD licensed and designed to provide both a consistant interface for managing content, and a simple architecture that makes diving in and hacking on the code as easy as possible.

Its goal is to resemble something like `Wordpress`_, with an intuitive interface for managing pages and blog posts. Mezzanine takes a different approach from other Django applications in this space like `Pinax`_ or `Mingus`_ that glue together a lot of reusable apps, instead opting to provide most of its functionality included with the project by default.

Features
--------

On top of all the usual features provided by Django such as MVC architecture, ORM, templating, caching and the automatic admin interface, Mezzanine provides the following features.

  * Hierarchical page navigation
  * Save as draft and preview on site
  * Scheduled publishing
  * Drag-n-drop page ordering
  * WYSIWYG editing
  * API for custom content types
  * SEO friendly URLs and meta data
  * Mobile device detection and templates
  * Blogging engine
  * Tagging
  * Built-in threaded comments, or:
  * `Disqus`_ integration
  * `Gravatar`_ integration
  * `Google Analytics`_ integration
  * `Twitter`_ feed integration
  * `bit.ly`_ integration
  * Sharing via Facebook or Twitter
  * Custom templates per page or blog post
  * Built-in test suite

The Mezzanine admin dashboard:

.. image:: http://media.tumblr.com/tumblr_l3su7jFBHM1qa0qji.png

Dependencies
------------

Apart from `Django`_ itself, Mezzanine has no explicit dependencies but is designed to be used most effectively in conjunction with the following libraries.

  * `setuptools`_
  * `Python Imaging Library`_ (PIL)
  * `django-grappelli`_ <= 2.0
  * `django-filebrowser`_ <= 3.0

Installation
------------

Assuming you have `setuptools`_ installed, the easiest method is to install directly from pypi by running the following command, which will also attempt to install the dependencies mentioned above::

    $ easy_install -U mezzanine

Otherwise you can download Mezzanine and install it directly from source::

    $ python setup.py install
    
Once installed, the command ``mezzanine-project`` should be available which can be used for creating a new Mezzaine project in a similar fashion to ``django-admin.py``::

    $ mezzanine-project project_name

You can then run your project with the usual Django steps::

    $ cd project_name
    $ ./manage.py syncdb
    $ ./manage.py runserver

Contributing
------------

Mezzanine is an open source project that is managed using both Git and Mercurial version control systems. These repositories are hosted on both `Github`_ and `Bitbucket`_ respectively, so contributing is as easy as forking the project on either of these sites and committing back your enhancements. 

Support
-------

For questions, comments, feature requests or bugs reports please join the `mezzanine-users`_ mailing list. 

Sites Using Mezzanine
---------------------

  * `Citrus Agency`_

Quotes
------

  * "Who came up with the name Mezzanine? I love it, like a platform between the client's ideas and their published website. Very classy!" - `swhite`_

.. _`Django`: http://djangoproject.com/
.. _`Wordpress`: http://wordpress.org/
.. _`Pinax`: http://pinaxproject.com/
.. _`Mingus`: http://github.com/montylounge/django-mingus
.. _`setuptools`: http://pypi.python.org/pypi/setuptools
.. _`Python Imaging Library`: http://www.pythonware.com/products/pil/
.. _`django-grappelli`: http://code.google.com/p/django-grappelli/
.. _`django-filebrowser`: http://code.google.com/p/django-filebrowser/
.. _`Disqus`: http://disqus.com/
.. _`Gravatar`: http://gravatar.com/
.. _`Google Analytics`: http://www.google.com/analytics/
.. _`Twitter`: http://twitter.com/
.. _`bit.ly`: http://bit.ly/
.. _`Citrus Agency`: http://citrus.com.au/
.. _`swhite`: http://bitbucket.org/swhite/
.. _`Github`: http://github.com/stephenmcd/mezzanine/
.. _`Bitbucket`: http://bitbucket.org/stephenmcd/mezzanine/
.. _`mezzanine-users`: http://groups.google.com/group/mezzanine-users

