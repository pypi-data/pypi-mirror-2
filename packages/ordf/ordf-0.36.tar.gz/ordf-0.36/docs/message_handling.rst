
Messaging and Storage Subsystem
===============================

Why are the seemingly different facilities of message passing and storage in one module?
Because on the one hand, a storage back-end or index is basically a thin wrapper around
some implementation library, and on the other hand it is the function of the messaging
subsystem to hand any new or changed graphs off to these back-ends for storage or indexing.

Perhaps this will be more understandable with an ascii-art diagram::

  +-----------+     +---------+     +---------+
  | new Graph |---->| Handler |---->| Storage |
  +-----------+     +---------+     +---------+
                          \      +---------+
                           \---->| Index 1 |
                            \    +---------+
	                     \      +---------+
                              \---->| Index 2 |
                               \    +---------+
                                \      +---------+
                                 \---->| Index n |
                                       +---------+

Each storage and index back-end implements the same interface, a handful
of methods that are explained in detail in the :class:`HandlerPlugin` 
documentation that basically take *Graphs* or *ChangeSets* and put them
into some sort of storage.

Back-ends may be registered for reading or for writing and it is quite
possible to construct a distributed system where the main :class:`Handler`
of, say, a web application simply passes newly created or changed graphs
to a back-end that sends it into a message queueing system. If done in
this way, each storage and index back-end can be run as an autonomous
daemon listening to a queue and indices can be updated asynchronously.

::

    +-------+     +---------+     +-------------+
    | Graph |---->| Handler |---->| RabbitQueue |
    +-------+     +---------+     +-------------+
                            ,............/
                           /
                     +----------+
                     | RabbitMQ |
                     +----------+
                 ,......../
                /
    +---------------+     +-------- ... ------+
    | RabbitHandler |---->| Storage ... Index |
    +---------------+     +-------- ... ------+


This is precicely what :mod:`ordf.handler.queue` implements. The
:class:`ordf.handler.queue.RabbitHandler` behaves just like a normal
:class:`ordf.handler.Handler` except that instead of waiting for its
*put* method to be called, it listens to a queue which calls put
appropriately for each received message.

.. toctree::
   :maxdepth: 2

   ordf_handler
   ordf_handler_pt
   ordf_handler_rdf
   ordf_handler_xapian
   ordf_handler_queue
   ordf_handler_fuxi
