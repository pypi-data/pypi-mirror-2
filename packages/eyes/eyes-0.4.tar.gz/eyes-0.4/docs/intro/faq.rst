.. _faq-index:

========
Eyes FAQ
========
   
Why does this project exist?
----------------------------

How do I do X? Why doesn't Y work? Where can I go to get help?
--------------------------------------------------------------

If this FAQ doesn't contain an answer to your question, you might want to
try the `eyes-users mailing list`_. Feel free to ask any question related
to installing, using, or debugging Eyes.

If you prefer IRC, the `#eyes IRC channel`_ on the Freenode IRC network is an
active community of helpful individuals who may be able to solve your problem.

.. _`eyes-users mailing list`: http://groups.google.com/group/eyes-users
.. _`#eyes IRC channel`: irc://irc.freenode.net/eyes

How do I get started?
---------------------

    #. `Download the code`_.
    #. Install Django (read the :ref:`installation guide <intro-install>`).
    #. Check out the rest of the :ref:`documentation <index>`, and ask questions if you
       run into trouble.

.. _`Download the code`: http://bitbucket.org/heckj/eyes/src/

What are Eyes's prerequisites?
--------------------------------

Eyes requires
* Python_ 2.4 or later.
* Django_ 1.2 or later

For a development environment -- if you just want to experiment with Django --
you don't need to have a separate Web server installed; Django comes with its
own lightweight development server. For a production environment, we recommend
`Apache 2`_ and mod_python_, although Django follows the WSGI_ spec, which
means it can run on a variety of server platforms.

Using Django requires a database. PostgreSQL_, MySQL_, `SQLite 3`_, and Oracle_ are supported.

.. _Django: http://www.djangoproject.com/
.. _Python: http://www.python.org/
.. _Apache 2: http://httpd.apache.org/
.. _mod_python: http://www.modpython.org/
.. _WSGI: http://www.python.org/peps/pep-0333.html
.. _PostgreSQL: http://www.postgresql.org/
.. _MySQL: http://www.mysql.com/
.. _`SQLite 3`: http://www.sqlite.org/
.. _Oracle: http://www.oracle.com/