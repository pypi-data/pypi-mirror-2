django-icecast-balancer
=======================

A easy to set up HTTP load balancer for Icecast2 servers using the Django 
framework. It redirects clients like VLC or Xine along several instances of 
Icecast2 providing the same stream.


How it works
------------
  The application itself polls all configured Icecast2 servers for free slots 
  on their streams and uses HTTP redirects (302) to distribute clients to free 
  streaming slots. Selection of free slots is based on GeoIP support if available.

Download
--------
  http://pypi.python.org/

Installation
------------
From source:
  1. Download the tar.gz file
  2. Extract it: tar xfz django-icecast-balancer-.tar.gz
  3. Run the setup: python django-icecast-balancer-/setup.py install 

Debian package:
  Install the package from http://debian.fladi.at/.

Integration
-----------
Django
~~~~~~
  ALERT! This example is using the Django runserver command which is only intended 
  for development, not for production use. If you are looking for a way to provide 
  icecast_balancer in a high-demand environment, take a look at mod_wsgi which is 
  much more suitable. 

  Add icecast_balancer to INSTALLED_APPS in settings.py and a URL mapping in urls.py 
  for the balancer in your project:

    urlpatterns = patterns('',
        (r'^icecast_balancer/', include('icecast_balancer.urls')),
    )

  After that synchronize the database:

    django-admin syncdb --settings=my_weave_server.settings --pythonpath=.

  Run the development server:

    django-admin runserver --settings=my_weave_server.settings --pythonpath=.

Icecast2 XSLT interface
~~~~~~~~~~~~~~~~~~~~~~~
  The load-balancer needs to be able to periodically poll the status of the configured 
  Icecast2 servers. Therefor the package includes the file load.xsl. This file needs to 
  be copied to the web root of each Icecast2 server that will take part in the load-balancer. 
  For Debian this location is at /usr/share/icecast2/web/. To test if the file is at the 
  right location open the URL to the Icecast2 server in the browser and attach load.xsl 
  to it like this:

    http://<icecast2-ip>:<icecast2-port>/load.xsl 

  The output should look something like this:

    <load>
      <mount name="/fm4-hq.ogg">32</mount>
      <mount name="/fm4-lq.ogg">96</mount>
      <mount name="/fm4-mq.ogg">64</mount>
    </load>

  If there is an error stating "The file you requested could not be found" the file 
  is probably not in the right folder.

Updating the servers
--------------------
Create a new cronjob for the user running the Django project:

  */5 * * * * python path/to/project/manage.py icecastpoll --settings=project.settings

  An interval of 5 minutes as shown in the above example should be sufficient but it 
  can be decreased down to 1 minute.

Celery
~~~~~~
  If the Django project includes a working setup for Celery the management command 
  "icecastpoll" will automatically dispatch the update as a async task. The cronjob 
  is still required to trigger the updates.

Usage
-----
  Got to the admin interface of the Django instance. There are now three models for 
  the icecast_balancer application:
    * Mounts
    * Servers
    * Streams 

  Populate them with the servers and streams to match the actual Icecast setup.

  Once everything is setup up correctly test the load-balancer by opening a stream 
  in your favourite video player:

    http://<django-hostname>/icecast_balancer/<stream-name>/

  The player will now be redirected to a Icecast2 server and the stream will be 
  played from there. 
  
Feedback
--------

Use `Issue Tracker on Google Code`__ for the bug reports / feature requests.

Contact me directly at michael@fladi.at.

__ http://code.google.com/p/django-icecast-balancer/issues/list