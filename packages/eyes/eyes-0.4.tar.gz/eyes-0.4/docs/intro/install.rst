.. _intro-install:

Install guide
===================

Before you can use Eyes, you'll need to get it installed. This guide will guide you to a simple, minimal installation that'll work while you walk through the introduction.

Ubuntu 9.10
-----------

These instructions are specific to setting up an instance starting with a bare-bones Ubuntu 9.10 Server instance.

Connect to the host as root, and upgrade to the latest::

 apt-get update
 apt-get dist-upgrade
 apt-get install openssh-server
 apt-get install nagios-plugins rrdtool python-dev python-pip python-setuptools
 apt-get install python-distutils-extra python-memcache python-openssl
 apt-get install python-mysqldb mysql-server memcached
 apt-get install nginx python-flup

Now we'll get some expected and needed python libraries::

 pip install simplejson
 pip install httplib2
 pip install elementtree
 pip install pyrrd
 pip install django
 pip install python-dateutil
 pip install South

Enable memcached
----------------

edit /etc/default/memcached::

 # Set this to yes to enable memcached.
 ENABLE_MEMCACHED=yes

start memcached::

 service memcached start

Installing from Development
---------------------------

Set up a MySQL database for eyes::

 mysql -u root -p
 CREATE DATABASE eyesdb CHARACTER SET utf8;
 CREATE USER eyes IDENTIFIED BY 'eyes345';
 GRANT ALL PRIVILEGES ON *.* to 'eyes'@'localhost' IDENTIFIED BY 'eyes345';
 FLUSH PRIVILEGES;

Get mercurial to download the latest from source::

 apt-get install mercurial

Set up an account and directory to house the application::

 adduser eyes
 su - eyes
 hg clone http://bitbucket.org/heckj/eyes

Make a link for the django admin media::

 cd eyes/eyeswebapp
 ln -s /usr/local/lib/python2.6/dist-packages/django/contrib/admin/media/
 exit

Configure nginx by creating /etc/nginx/sites-available/eyes::

 upstream djangoserv {
   server 127.0.0.1:8801;
 }
 
 server {
   listen 80;
   root /home/eyes/eyes/eyeswebapp;
 
   location /static_media {
     root /home/eyes/eyes/eyeswebapp;
     autoindex on;
   }
 
   location ~* ^.+\.(jpg|jpeg|gif|png|ico|css|zip|tgz|gz|rar|bz2|doc|xls|exe|pdf|ppt|txt|tar|mid|midi|wav|bmp|rtf|js|mov) {
     access_log   off;
     expires      30d;
   }
 
   location / {
     # host and port to fastcgi server
     fastcgi_pass 127.0.0.1:8801;
     fastcgi_param PATH_INFO $fastcgi_script_name;
     fastcgi_param REQUEST_METHOD $request_method;
     fastcgi_param QUERY_STRING $query_string;
     fastcgi_param SERVER_NAME $server_name;
     fastcgi_param SERVER_PORT $server_port;
     fastcgi_param SERVER_PROTOCOL $server_protocol;
     fastcgi_param CONTENT_TYPE $content_type;
     fastcgi_param CONTENT_LENGTH $content_length;
     fastcgi_pass_header Authorization;
     fastcgi_intercept_errors off;
   }
 }

Disable the default site and enable eyes::

 cd /etc/nginx/sites-enabled/
 rm default
 ln -s /etc/nginx/sites-available/eyes

Start nginx::

 service nginx start

Update the settings and establish the Fire up the django application::

 su - eyes
 cd eyes/eyeswebapp/

edit settings.py
----------------

first set up the database fields::

 DATABASE_ENGINE = 'mysql'  # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
 DATABASE_NAME = 'eyesdb'           # Or path to database file if using sqlite3.
 DATABASE_USER = 'eyes'             # Not used with sqlite3.
 DATABASE_PASSWORD = 'eyes345'      # Not used with sqlite3.
 DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
 DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

then enable the caching backend::

 CACHE_BACKEND = "memcached://127.0.0.1:11211/?timeout=60"

Validate and initialize
-----------------------

set up the database::

 python manage.py validate
 python manage.py syncdb --noinput
 python manage.py createsuperuser --username=admin --email=admin@localhost.com --noinput
 python setsuperuserpassword.py

Run the server::

 python manage.py runfcgi method=threaded host=127.0.0.1 port=8801

Start the local poller::

 nohup python util/poster.py &

Log in and go from there:
-------------------------

Now log in to the site:

* navigate a browser to http://your_site.com/admin/
* initial user is "admin", password "admin"

* Go to http://your_site.com/admin/auth/user/1/ to update the admin user's email and password
* Go to http://your_site.com/admin/sites/site/1/ and update the site name to your local site name

Getting updates from source
---------------------------

To get the updates from source, update using mercurial::

 su - eyes
 cd eyes
 hg pull
 hg update

If you have made local copies, 'hg update' may not work, in which case you should::

 hg merge
 hg commit

 python manage.py migrate

You can always see the log of changes with::

 hg log

