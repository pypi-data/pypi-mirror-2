Getting Started
===============

Please keep in mind that this software is under active development. It is
stabilising with respect to the API interface but there are no guarantees!
We are always happy to hear of the experiences of anyone who tries to get
going with ORDF, stories of success or failure, but reports and suggestions,
are encouraged via the `usual channels`_.

.. _usual channels: http://okfn.org/contact

Installation
------------

ORDF is available from a mercurial repository::

     http://ordf.org/src/

The usual way of installing is to use `virtualenv`_ and `pip`_. Setting up
a basic environment is easy::

    % virtualenv /work
    % . /work/bin/activate
    (ordf)% pip install ordf

If you want to use the `FuXi`_ reasoner and/or RDFLib's SPARQL support
then you should now run::

    (ordf)% pip uninstall rdflib
    (ordf)% pip install rdflib==2.4.2

If you do not need reasoning and want to use another SPARQL implementation
(e.g. `4store`_) then you should be able to run with the neweer 3.0.0
version of rdflib

If you are using 4store, make sure to install the branch that supports
locking from http://github.com/wwaites/4store and the python bindings
from http://github.com/wwaites/py4s

For development you can do this instead of simply installing
the simpler *ordf*::

    (ordf)% pip install mercurial
    (ordf)% pip install -e hg+http://ordf.org/src/#egg=ordf

Once you have done this, you should have the ordf source checked out in
*/work/src/ordf*.

.. _virtualenv: http://pypi.python.org/pypi/virtualenv
.. _pip: http://pip.openplans.org/
.. _RDFLib: http://www.rdflib.net/
.. _FuXi: http://code.google.com/p/fuxi/
.. _4store: http://4store.org/

Running the Tests
-----------------

To run the tests, you have to installed the development branch.
In the source directory */work/src/ordf* do::

    (ordf)% pip install nose
    (ordf)% python setup.py nosetests --verbosity=2 -s

*NOTE*: to run the fourstore tests you need to have a
4store instance serving a kb called ordf_test. To do
this::

    % 4s-backend-setup ordf_test
    % 4s-backend ordf_test

Also make sure to install py4s from http://github.com/wwaites/py4s
This requires at least version 0.8
Also see http://wiki.github.com/wwaites/py4s/installing-py4s

*NOTE*: to run the rabbitmq tests, rabbitmq-server needs to
be running with an exchange ordf_test that can be accessed
by the user guest/guest.

Building Documentation
----------------------

To build this documentation::

    (myenv)% pip install sphinx
    (myenv)% python setup.py build_sphinx

and the documentation will be in */work/src/ordf/build/sphinx/html/index.html*

Configuration
-------------

There are two usual modes of operation for using *ordf*. The first is
to use it as a library in another program, for example a Pylons_ application.
The second is via an included command line program called :program:`ordf`.
There are example configurations in http://ordf.org/src/file/tip/examples/
*simple.ini* is good for getting quickly started with some persistent 
storage.

A Testing Environment
---------------------

A very simple configuration for a Pylons_ application might be to just do
any indexing and saving in the web request processing thread. This might not
scale very well, particularly if adding a document to an index is a time
consuming operation, but it is typical for a development environment. A
fragment of an appropriate *development.ini*::

    ordf.readers = pairtree
    ordf.writers = pairtree,fourstore,xapian

    pairtree.args = %(here)s/data/pairtree
    fourstore.args = somekb
    xapian.args = 127.0.0.1:44332

If you are using the :class:`~ordf.handler.rdf.FourStore` back-end, it is
important to use the `locking 4store branch` and to have the `py4s bindings`
installed. Native `RDFLib`_ storage can also be used by putting *rdflib*
in place of *fourstore* in *ordf.writers* and configuring it with::

    rdflib.args = %(here)s/data/rdflib_sleepycat
    rdflib.store = Sleepycat

The Xapian_ back-end is usually run as a network daemon using the *xapian-tcpsrv*
command. This takes care of marshalling read and write operations to the 
database so that we don't have to do it ourselves. It is possible to run
directly from the filesystem but it is likely that you will experience locking
errors if you try.

A Production Environment
------------------------

A production installation will normally have a message queueing service such
as `RabbitMQ`_ and a front-end interface will be configured to send messages
to it. There will be several back-end storage modules that each listen to a
queue and take any action required whenever a message arrives. Please refer
to the `RabbitMQ documentation`_ for instructions for installing and setting
up the queueing daemon.

It is important to distinguish between back-ends used for reading and for 
writing. For example, a typical configuration fragment from a Pylons_ 
application might be::

    ordf.readers = pairtree,fourstore,xapian
    ordf.writers = rabbit

    pairtree.args = %(here)s/data/pairtree
    fourstore.args = somekb
    xapian.args = 127.0.0.1:44332

    rabbit.hostname = localhost
    rabbit.userid = guest
    rabbit.password = guest
    rabbit.connect.exchange = changes

In this setup, the various back-ends are set-up for read-only operation, but
they are still available to the :class:`~ordf.handler.Handler` singleton in
the application. Any write operations, however, are sent to the message 
queue for processing.

Note that because :class:`~ordf.handler.pt.PairTree` is used for reading it
is expected that the storage is available on the local disk or via NFS or
some other mechanism. If any other indices need access to it and they are
actually running on another host, suitable arrangements will need to be 
made.

Also the situation with respect to :class:`~ordf.handler.rdf.FourStore` 
and :class:`~ordf.handler.xap.Xapian` described above in the context of a
development environment is the same here.

At this point we have a Pylons_ application running and reading information
from the back-ends and any write operations are sitting in a queue waiting
to be processed. For each of the back-ends we need to make a configuration
file and then use the :program:`ordf` program to run them.

Taking the :class:`ordf.handler.rdf.PairTree` back-end first, an appropriate
configuration file for :program:`ordf` might look something like::

    [app:main]

    ordf.handler = ordf.handler.queue:RabbitHandler
    ordf.handler.hostname = localhost
    ordf.handler.userid = guest
    ordf.handler.password = guest
    ordf.connect.queue = pairtree

    ordf.writers = pairtree
    pairtree.args = /some/where/data/pairtree

We would then run :program:`ordf` like so::

   ordf -c pairtree.ini -l /var/log/ordf/pairtree.log

A similar arrangement would be used for the other back-ends, the main difference
being the *ordf.writers* directive and any arguments that the back-end requires.

.. _configuring-inferencing:

Configuring Inferencing
-----------------------

Configuring inferencing is slightly complicated because it normally involves
listening to one message exchange and writing to another. A configuration
file for :program:`ordf` might look like this::

     [app:main]

     ordf.handler = ordf.handler.queue:RabbitHandler
     ordf.handler.hostname = localhost
     ordf.handler.userid = guest
     ordf.handler.password = guest
     ordf.connect.exchange = reason
     ordf.connect.queue = fuxi

     ordf.readers = fuxi,pairtree
     ordf.writers = fuxi,rabbit

     fuxi.args = ordf.vocab.rdfs
     pairtree.args = /some/where/data/pairtree
     rabbit.hostname = localhost
     rabbit.userid = guest
     rabbit.password = guest
     rabbit.connect.exchange = index

This takes a little explaining. There are two exchanges, *reason* and *index*.
When a graph is saved, it is first sent to the *reason* exchange where
:program:`ordf` is listening with this configuration file.

The *fuxi* handler is an instance of :class:`ordf.handler.fuxi.FuXiReasoner` and
expects an already complete store containing one or more changesets and one or
more up-to-date graphs that they modify. The *fuxi.args* is a comma-separated
list of modules that export a :meth:`inference_rules` method that return rules
appropriate to that module. See the :ref:`inference-rules` section of this
manual.

When *fuxi* receives the store in its :meth:`~ordf.handler.fuxi.FuXiReasoner.put`
method it runs a production rule engine on all of the graphs that are not
changesets. It then makes a changeset that contains any new statements it was
able. It prevents the original changes from continuing to the *rabbit* handler
and substitutes the changeset it has made together with the original changes.

In this way, there will normally be two changesets -- the first containing the
original changes and the second containing inferred statements.

It is not a problem that *fuxi* makes a changeset that may be passed to its own
:meth:`~ordf.handler.fuxi.FuXiReasoner.put` method whilst in that method since
it is aware of this and simply returns without recursing and allows the *rabbit*
handler to forward the combined changes to the *index* exchange.

In order to give a richer set of facts to feed the inference engine, *fuxi*
needs access to other graphs that may be referenced by the original ones. For
example, given this rule and data (not bothering with namespaces)::

    { ?x :authorOf ?y } => { ?y :author ?x } .
    :LevTolstoy :authorOf :WarAndPeace .

*fuxi* can be expected to produce the triple::

    :WarAndPeace :author :LevTolstoy .

however the graph containing statements about *:WarAndPeace* may not be included
in the changes. The fact that *ordf.readers* contains *fuxi* and *pairtree* in
that order means that it will first look for the *:WarAndPeace* graph in *fuxi*
and then try *pairtree*.

Examples
--------

In addition to running the :program:`ordf` command line tool to listen to a queue and
update an index, it can be used for pulling a graph from the store, or saving a
graph to the store. The following configuration file can be used in both cases::

    [app:main]

    ordf.readers = pairtree
    ordf.writers = rabbit

    pairtree.args = /some/where/data/pairtree
    rabbit.hostname = localhost
    rabbit.userid = guest
    rabbit.password = guest
    rabbit.connect.exchange = index

This uses the message queueing system but so long as there aren't locking issues
to consider it could just as easily use a list of writers as in the development
environment above.

To retrieve a graph from the network or local filesystem and save it to the store::

   ordf -c cmdline.ini -s -m "import from dbpedia" \
   	 http://dbpedia.org/resource/Margaret_Fuller

To print out the same graph in N3 format::

   ordf -c cmdline.ini -t n3 http://dbpedia.org/resource/Margaret_Fuller

It is possible to use :program:`ordf` to (re)build one or more indices. For
example if there is data in a pairtree index and one decides to add 4store,
a configuration file like this named *mk4s.ini*::

    [app:main]

    ordf.readers = pairtree
    ordf.writers = fourstore

    pairtree.args = /some/where/data/pairtree
    fourstore.args = kbname

can be used with :program:`ordf` run like this::

    ordf -c mk4s.ini --reindex

to populate the new index. Only one reader may be specified in this
circumstance, but any number of writers may be used as usual.

.. _Pylons: http://pylonshq.com/
.. _RabbitMQ: http://www.rabbitmq.com/
.. _RabbitMQ documentation: http://www.rabbitmq.com/documentation.html
.. _Xapian: http://xapian.org/
.. _RDFLib: http://www.rdflib.net/
