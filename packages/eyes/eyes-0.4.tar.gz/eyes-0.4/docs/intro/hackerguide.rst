Hacker/Development Install Guide
=================================

Base Installation Pieces
===========================

MacOS X Development setup:
--------------------------

* *get and install MacPorts*
::

	sudo port install nagios-plugins rrdtool beanstalkd
	easy_install pip
	pip install virtualenv

Ubuntu (9.10) linux setup
-------------------------

*the follow should all be invoked as 'root'*

::

	apt-get update
	apt-get dist-upgrade
	apt-get install nagios-plugins mercurial rrdtool python-dev python-pip
	apt-get install avahi-daemon avahi-autoipd
	apt-get install build-essential
	apt-get install ubuntu-dev-tools
	apt-get install git-core
	apt-get install subversion
	apt-get install openssh-server
	apt-get install fping
	apt-get install python-setuptools python-distutils-extra
	apt-get install pylint pyflakes
	apt-get install python-openssl
	apt-get install python-memcache
	apt-get install python-virtualenv
	easy_install pip

CentOS (5.4) linux setup
-------------------------

::

	yum -y update
	yum install nagios-plugins mercurial rrdtool
	yum install python-dev python-pip

Setting up for development
==========================

Set up a VirtualEnv for working with the project
------------------------------------------------

::

	cd ~/virtualenv
	pip install -E mon -U django

Check out the code into the virtualenv
--------------------------------------

::

	cd ~/virtualenv/mon
	hg clone http://bitbucket.org/heckj/eyes/
	source bin/activate

Install the required libraries
------------------------------

::

	pip install -r eyes/requirements.txt

Verify by running the tests
---------------------------

::

	cd ~/virtualenv/mon/eyes
	make clean
	make test

Working with the code:
----------------------

::

	cd ~/virtualenv/mon/eyes/eyeswebapp
	python manage.py validate # *validates django config & models*)
	./reset.bash && python util/simplepoller.py # *resets database to latest scheme, loads data, and runs poller*
	python manage.py shell # *access django shell*
	python manage.py runserver # *fire up the django server @ http://localhost:8000/*

Useful links:
-------------

* pyrrd source: http://code.google.com/p/pyrrd/source/browse/trunk/pyrrd/
* pyrrd example: http://code.google.com/p/pyrrd/wiki/MoreDetails
* working with time Wiki page: http://wiki.python.org/moin/WorkingWithTime
* python dateutil: http://labix.org/python-dateutil
* Piston home: http://bitbucket.org/jespern/django-piston
* Piston documentation: http://bitbucket.org/jespern/django-piston/wiki/Documentation

Running the simplest setup:
---------------------------

::

	cd eyeswebapp
	./reset.bash && python util/simplepoller.py
	does a local ping (initial data model loaded from modeltestdata.json) and stores the results into RRD files
	default location (now) for RRD files is under ./tmp_rrd/ directory. 
	default location (now) for PNG files is under ./tmp_png/ directory. 

Testing in sections
-------------------

::

	cd eyeswebapp
	python manage.py test util
	python manage.py test core
	python manage.py test api

Migrating database changes with South
-------------------------------------

::

	python manage.py migrate

Pulling updated code from the repository
----------------------------------------

::

	cd ~/virtualenv/mon
	source bin/activate
	cd eyes
	hg incoming

*this command will show you any pending changes to be pulled down and merged*

To retrieve those updates:

::

	hg fetch

Pushing code into the repository
--------------------------------

* *establish base working from latest code...*::
	cd ~/virtualenv/mon
	source bin/activate
	cd eyes
	hg incoming

* *do your coding, etc*

* *if you've changed any of the models or database elements of the code*::

	./manage.py startmigration <app_name> <migration_name> --auto_

* *for example, if you edited the models in the application "asset", you might use*::

	./manage.py startmigration asset done_something_asset --auto
	./manage.py migrate

* *if you've created a new application*::

	./manage.py startmigration <app_name> <migration_name> --initial_

* for example, if you created the application "about", you might use::

	./manage.py startmigration about initial_about --initial`
	hg st
	hg add
	./manage.py test util core api

* *any other baseline tests that have been established*::

	hg commit
	hg push


Working with migrations as you develop
--------------------------------------

The project includes South, which is a framework for dealing with schema transitions and migrations
while a project is under active development. South will only track applications for schema migration
that we've identified. Sspecifically, it looks for a folder called 'migrations' in the application 
directory; the same level as the `models.py` file.

* see also: http://south.aeracode.org/wiki/Documentation
* see also: http://south.aeracode.org/wiki/Tutorial1
* see also: http://ericholscher.com/blog/2009/jun/11/migrating-test-fixtures-using-south/
* see also: http://stackoverflow.com/questions/44109/extending-the-user-model-with-custom-fields-in-django

When you create any new application in which want to track schema migrations
----------------------------------------------------------------------------

* create the application::

	./manage.py startapplication appname

* move the application under the 'apps' folder to keep things clean::

	mv appname apps

* set up an initial migration::

	./manage.py schemamigration appname --initial

When you're changing that model
-------------------------------

* edit the models.py file

* create a migration to change the schema::

	./manage.py schemamigration appname add_something_to_model --auto

the "add\_something\_to\_model" should be a descriptive name of the change that you've just made - adding a model, adding a field to a model, or whatever is appropriate. This command will identify all the changes that it can find in the model since the latest migration and create a new migration file for it.

* create a migration to update/change data

if you're making a migration that needs to edit data (say a site update where data in the schema is changing), then the south project recommends that you create a separate migration that just manipulates the data. To create the base mgiration file for editing, use the command::

	./manage.py datamigration appname change_data_description

the "change\_data\_description" is again meant to be a descriptive name of the change you're making. Running this command will tell you what migration file was created. An example from our project:::

	./manage.py startmigration asset blank_migration

creates the file::

	from south.db import db
	from django.db import models
	from asset.models import *

	class Migration:

	    def forwards(self, orm):
	        "Write your forwards migration here"


	    def backwards(self, orm):
	        "Write your backwards migration here"


	    models = {
	        'asset.activity': {
	            'Asset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['asset.Asset']"}),
	            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
	        },
	        'asset.asset': {
	            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
	            'type': ('django.db.models.fields.CharField', [], {'max_length': '120'})
	        },
	        'asset.car': {
	            'asset_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['asset.Asset']", 'unique': 'True', 'primary_key': 'True'}),
	            'make': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
	            'model': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
	            'year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
	        }
	    }

	    complete_apps = ['asset']

To migrate data, you should write in methods for "forwards" and "backwards" that allow for the data to be changed. For example:::

	def forwards(self, orm):
		"Write your forwards migration here"
		for asset in orm.Asset.objects.all():
			asset.type = 'example'
			asset.save()

	def backwards(self, orm):
		"Write your backwards migration here"
		for asset in orm.Asset.objects.all():
			asset.type = ''
			asset.save()

* << edit the core/models.py file >>
::
	python manage.py schemamigration core remove_hostip --auto
* * if you've made a model change that can lead to inconsistencies, the result might be an error that will request that you make some decisions about the model and try again.
* verify file created at core/migrations/*
* if all looks good migrate:

::
	python manage.py migrate
* add into source control

::
	hg add core/migrations/*
	hg commit -m "adding migration for ..."

Setting up Continuous Integration (using Hudson)
================================================

I'm using the write up on setting up Hudson for python projects at http://www.rhonabwy.com/wp/2009/11/04/setting-up-a-python-ci-server-with-hudson/

* wget http://hudson-ci.org/latest/hudson.war
* java -jar hudson.war
* open http://localhost:8080/manage
* (upgrade to the latest version of hudson if you like)
* http://localhost:8080/pluginManager/
* * Install the following plugins:
* * * Mercurial Plugin
* * * Python Plugin
* * * Violations Plugin
* * Create a new job (http://localhost:8080/view/All/newJob)
* * * free-style project, named "Eyes"
* * * add a build step
* * * * Execute Shell
* * * * * make test
* * * Mercurial project
* * * * repository url: http://bitbucket.org/heckj/eyes/
* * * Aggregate downstream test results
* * * * Automatically aggregate all downstream tests
* * * Publish JUnit test result report
* * * * \**/testresults/*.xml
* * * Report Violations
* * * * pylint 10,999,**/reports/pylint.txt
* * * corbertura plugin
* * * * pip install coverage
* * * * corbertura \**/reports/coverage.xml

Notes on using Nagios Plugins
-----------------------------

check_ping::

	[internalcheck:/opt/local/libexec/nagios] heckj$ ./check_ping -H localhost -w 1,99% -c 1,99%
	PING OK - Packet loss = 0%, RTA = 0.18 ms|rta=0.182000ms;1.000000;1.000000;0.000000 pl=0%;99;99;0

check_fping::

	[internalcheck:/opt/local/libexec/nagios] heckj$ ./check_fping -H localhost 
	FPING OK - localhost (loss=0%, rta=0.090000 ms)|loss=0%;;;0;100 rta=0.000090s;;;0.000000
	[internalcheck:/opt/local/libexec/nagios] heckj$ ./check_fping -H localhost -w 1,99% -c 1,99%
	FPING OK - localhost (loss=0%, rta=0.110000 ms)|loss=0%;99;99;0;100 rta=0.000110s;0.001000;0.001000;0.000000

check_http::

	Usage: check_http -H <vhost> | -I <IP-address> [-u <uri>] [-p <port>]
	       [-w <warn time>] [-c <critical time>] [-t <timeout>] [-L]
	       [-a auth] [-f <ok | warn | critcal | follow>] [-e <expect>]
	       [-s string] [-l] [-r <regex> | -R <case-insensitive regex>] [-P string]
	       [-m <min_pg_size>:<max_pg_size>] [-4|-6] [-N] [-M <age>] [-A string]
	       [-k string] [-S] [-C <age>] [-T <content-type>]

	[internalcheck:/opt/local/libexec/nagios] heckj$ ./check_http -H localhost -p 8080
	HTTP OK HTTP/1.0 200 OK - 10372 bytes in 0.163 seconds |time=0.163247s;;;0.000000 size=10372B;;;0

check_snmp::

	Usage:check_snmp -H <ip_address> -o <OID> [-w warn_range] [-c crit_range]
	[-C community] [-s string] [-r regex] [-R regexi] [-t timeout] [-e retries]
	[-l label] [-u units] [-p port-number] [-d delimiter] [-D output-delimiter]
	[-m miblist] [-P snmp version] [-L seclevel] [-U secname] [-a authproto]
	[-A authpasswd] [-X privpasswd]

check_tcp::

	Usage:check_tcp -H host -p port [-w <warning time>] [-c <critical time>] [-s <send string>]
	[-e <expect string>] [-q <quit string>][-m <maximum bytes>] [-d <delay>]
	[-t <timeout seconds>] [-r <refuse state>] [-M <mismatch state>] [-v] [-4|-6] [-j]
	[-D <days to cert expiry>] [-S <use SSL>] [-E]
	[internalcheck:/opt/local/libexec/nagios] heckj$ ./check_tcp -S -H bitbucket.org -p 443
	TCP OK - 0.419 second response time on port 443|time=0.418755s;;;0.000000;10.000000

Data structures using util.nagios.NagiosPoller()
================================================

Example results:

>>> xyz = NagiosPoller()
>>> ping_argset = ArgSet()
>>> ping_argset.add_argument_pair("-H", "localhost")
>>> ping_argset.add_argument_pair("-w", "1,99%")
>>> ping_argset.add_argument_pair("-c", "1,99%")
>>> result_dict = xyz.run_plugin('check_ping', ping_argset)
>>> print pprint.pformat(result_dict)

::

	{'command': '/opt/local/libexec/nagios/check_ping -H localhost -w 1,99% -c 1,99%',
	 'decoded': {'human': 'PING OK - Packet loss = 0%, RTA = 0.11 ms',
	             'pl': {'UOM': '%',
	                    'critvalue': '99',
	                    'label': 'pl',
	                    'maxvalue': '',
	                    'minvalue': '0',
	                    'value': '0',
	                    'warnvalue': '99'},
	             'rta': {'UOM': 'ms',
	                     'critvalue': '1.000000',
	                     'label': 'rta',
	                     'maxvalue': '',
	                     'minvalue': '0.000000',
	                     'value': '0.113000',
	                     'warnvalue': '1.000000'}},
	 'error': None,
	 'output': 'PING OK - Packet loss = 0%, RTA = 0.11 ms|rta=0.113000ms;1.000000;1.000000;0.000000 pl=0%;99;99;0',
	 'returncode': 0,
	 'timestamp': '2009-11-07T16:43:46.696214'}
 
>>> abc = NagiosPoller()
>>> http_argset = ArgSet()
>>> http_argset.add_argument_pair("-H", "www.google.com")
>>> http_argset.add_argument_pair("-p", "80")
>>> result_dict = abc.run_plugin('check_http', http_argset)
>>> print pprint.pformat(result_dict)

::

	{'command': '/opt/local/libexec/nagios/check_http -H www.google.com -p 80',
	 'decoded': {'human': 'HTTP OK HTTP/1.0 200 OK - 5825 bytes in 2.158 seconds ',
	             'size': {'UOM': 'B',
	                      'critvalue': '',
	                      'label': 'size',
	                      'maxvalue': '',
	                      'minvalue': '0',
	                      'value': '5825',
	                      'warnvalue': ''},
	             'time': {'UOM': 's',
	                      'critvalue': '',
	                      'label': 'time',
	                      'maxvalue': '',
	                      'minvalue': '0.000000',
	                      'value': '2.157739',
	                      'warnvalue': ''}},
	 'error': None,
	 'output': 'HTTP OK HTTP/1.0 200 OK - 5825 bytes in 2.158 seconds |time=2.157739s;;;0.000000 size=5825B;;;0',
	 'returncode': 0,
	 'timestamp': '2009-11-07T16:43:48.985950'}
