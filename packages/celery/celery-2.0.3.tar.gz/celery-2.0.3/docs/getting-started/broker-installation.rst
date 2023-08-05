=====================
 Broker Installation
=====================

.. contents::
    :local:

Installing RabbitMQ
===================

See `Installing RabbitMQ`_ over at RabbitMQ's website. For Mac OS X
see `Installing RabbitMQ on OS X`_.

.. _`Installing RabbitMQ`: http://www.rabbitmq.com/install.html

Setting up RabbitMQ
===================

To use celery we need to create a RabbitMQ user, a virtual host and
allow that user access to that virtual host::

    $ rabbitmqctl add_user myuser mypassword

    $ rabbitmqctl add_vhost myvhost

    $ rabbitmqctl set_permissions -p myvhost myuser ".*" ".*" ".*"

See the RabbitMQ `Admin Guide`_ for more information about `access control`_.

.. _`Admin Guide`: http://www.rabbitmq.com/admin-guide.html

.. _`access control`: http://www.rabbitmq.com/admin-guide.html#access-control


Installing RabbitMQ on OS X
===========================

The easiest way to install RabbitMQ on Snow Leopard is using `Homebrew`_; the new
and shiny package management system for OS X.

In this example we'll install homebrew into ``/lol``, but you can
choose whichever destination, even in your home directory if you want, as one of
the strengths of homebrew is that it's relocateable.

Homebrew is actually a `git`_ repository, so to install homebrew, you first need to
install git. Download and install from the disk image at
http://code.google.com/p/git-osx-installer/downloads/list?can=3

When git is installed you can finally clone the repo, storing it at the
``/lol`` location::

    $ git clone git://github.com/mxcl/homebrew /lol


Brew comes with a simple utility called ``brew``, used to install, remove and
query packages. To use it you first have to add it to ``PATH``, by
adding the following line to the end of your ``~/.profile``::

    export PATH="/lol/bin:/lol/sbin:$PATH"

Save your profile and reload it::

    $ source ~/.profile


Finally, we can install rabbitmq using ``brew``::

    $ brew install rabbitmq


.. _`Homebrew`: http://github.com/mxcl/homebrew/
.. _`git`: http://git-scm.org

Configuring the system hostname
-------------------------------

If you're using a DHCP server that is giving you a random hostname, you need
to permanently configure the hostname. This is because RabbitMQ uses the hostname
to communicate with nodes.

Use the ``scutil`` command to permanently set your hostname::

    sudo scutil --set HostName myhost.local

Then add that hostname to ``/etc/hosts`` so it's possible to resolve it
back into an IP address::

    127.0.0.1       localhost myhost myhost.local

If you start the rabbitmq server, your rabbit node should now be ``rabbit@myhost``,
as verified by ``rabbitmqctl``::

    $ sudo rabbitmqctl status
    Status of node rabbit@myhost ...
    [{running_applications,[{rabbit,"RabbitMQ","1.7.1"},
                        {mnesia,"MNESIA  CXC 138 12","4.4.12"},
                        {os_mon,"CPO  CXC 138 46","2.2.4"},
                        {sasl,"SASL  CXC 138 11","2.1.8"},
                        {stdlib,"ERTS  CXC 138 10","1.16.4"},
                        {kernel,"ERTS  CXC 138 10","2.13.4"}]},
    {nodes,[rabbit@myhost]},
    {running_nodes,[rabbit@myhost]}]
    ...done.

This is especially important if your DHCP server gives you a hostname
starting with an IP address, (e.g. ``23.10.112.31.comcast.net``), because
then RabbitMQ will try to use ``rabbit@23``, which is an illegal hostname.

Starting/Stopping the RabbitMQ server
-------------------------------------

To start the server::

    $ sudo rabbitmq-server

you can also run it in the background by adding the ``-detached`` option
(note: only one dash)::

    $ sudo rabbitmq-server -detached

Never use ``kill`` to stop the RabbitMQ server, but rather use the
``rabbitmqctl`` command::

    $ sudo rabbitmqctl stop

When the server is running, you can continue reading `Setting up RabbitMQ`_.

