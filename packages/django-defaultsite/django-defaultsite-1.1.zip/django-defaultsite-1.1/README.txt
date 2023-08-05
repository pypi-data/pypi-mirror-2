==================
django-defaultsite
==================

Sets the Site object in django to something better then example.com. So when other apps like pinax use it to construct email links that they actually work.

1. Installation.

To install either download the source and run 'setup.py install' like any other python module or install it from the cheese shop with 'easy_install django-defaultsite'

Then add 'defaultsite' into your INSTALLED_APPS in your django settings.

2. Configuration (Optional)

By default it will use socket.gethostname() to determine the host name of the site, and 'defaultsite' as the human readable version.

If you want to configure it further these settings are available, just put them in your settings.py:

SITE_ID: The primary key on which Site object to modify. Normally 1.

SITE_DOMAIN: The domain to use to replace 'example.com'. Defaults to your machine's hostname.

SITE_NAME: The sites name. Defaults to 'defaultsite'.
 