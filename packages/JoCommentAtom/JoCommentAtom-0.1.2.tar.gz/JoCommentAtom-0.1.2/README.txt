About JoCommentAtom
===================

JoCommentAtom is `Pyramid <http://docs.pylonshq.com/pyramid/dev/>`_
application maintained and developed by Jakub Warmuz that generates
`Atom feed <http://en.wikipedia.org/wiki/Atom_(standard)>`_ with the
latest comments from websites powered by `Joomla <http://www.joomla.org>`_
and `JoomlaComment extension <http://compojoom.com>`_.


Installation and Setup
======================

.. note::

    It is highly recommended to use `virtualenv
    <http://virtualenv.openplans.org>`_ in order create isolated Python
    evironment and not to install packages in the system-wide
    Python installation. You may also take a look at `virtualenvwrapper
    <http://www.doughellmann.com/projects/virtualenvwrapper/>`_.

#. Create a user in the Joomla's database and grant him an access to
   the following tables:

   - jos_comment (obviously, this is where all comments are stored)
   - jos_content (mandatory for proper URL generation for atom entries links)

#. Install JoCommentAtom using `pip <http://pip.openplans.org/>`_::

    $ pip install JoCommentAtom

   Or if you have downloaded an egg::

    $ easy_install JoCommentAtom.egg

   You may also want to install JoCommentAtom from source::

    $ python setup.py install

#. Create and edit configuration file to suit it Your needs::

    $ paster make-config --edit JoCommentAtom jocommentatom.ini

#. Run JoCommentAtom!::

    $ paster serve jocommentatom.ini

#. Or if You want to run JoCommentAtom as FastCGI process::

    $ paster serve --server-name=fcgi jocommentatom.ini

   Example FastCGI setup for `Nginx <http://wiki.nginx.org/HttpFcgiModule>`_
   HTTP server::

    server {
        listen :80;

        location / {
                fastcgi_pass 127.0.0.1:6543;
                fastcgi_param PATH_INFO $fastcgi_script_name;
        }
    }

#. Have fun!
