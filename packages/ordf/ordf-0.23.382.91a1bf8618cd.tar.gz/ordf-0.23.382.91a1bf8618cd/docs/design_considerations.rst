Design Considerations
=====================

Before going into the technical details of how the ORDF library 
works, perhaps it is helpful to explain some of what led us here.

.. toctree::
   :maxdepth: 2

The World Before RDF
--------------------

The story begins, really, with the CKAN_ software, which provides
a metadata registry for catalogueuing datasets. It is a
traditional Pylons_ application with a SQL back-end and all the
usual models and controllers and such. The basic design pattern
would be familiar to anyone who has ever used a MVC_ framework
such as Pylons_ or Django_ or `Ruby on Rails`_.

As the community expanded
others started running instances of the software. Where we 
started with a single site, now there is a decentralised network
of sites in Canada, Germany and elsewhere. Even some governments
are running their national data catalogues using it, for example
http://data.gov.uk/.

Perhaps unsurprisingly it was not long before members of this 
community began to want slight changes to the data model to suit
their local requirements. The most common request was to have
additional metadata for a package. There was no particular common
thread to the specific metadata each wanted so a system was 
devised to be able to add arbitrary key-value pairs to a package,
along with a way to specify how they were to be edited and 
validated.

This was a less than elegant solution, but it was simple and it
worked. Each site now has an extensions file that says what extra
pieces of data they want.

And then came the `INSPIRE Directive`_ which says that member
states of the European Union must make certain geographic data
available to the public. In order to be able to do this well, to
be able to add geographic metadata to catalogue entries and search
it with bounding boxes or circles we need to have a specialised
index on this metadata.

Making a spatial index is not hard, there is good support in 
PostGIS_, the GIS_ extensions for the PostgreSQL_ database that
we typically use, but it means that using a table of key-value
pairs is out and entails more extensive changes to the schema.

Worse, it risks introducing a dependency on PostGIS_ for sites 
that have no need of it -- sites outside of the EU that are not
concerned with geographic data.

It seemed like we were running up against the limits of the usual
SQL-backed MVC_ approach in trying to run a federated network of
data catalogues, each with their own local extensions and slightly
different requirements.

The particular drawbacks can be summarised:

    * SQL schemas are rigid. Making changes to the database schema
      means making parallel changes in the application code and
      making sure any running database is in sync.
    * Hacks like the table of key-value pairs to avoid divergent
      schemas at different sites forego efficient indexing and
      the expressivity otherwise possible with SQL for those fields.
    * Indexing of datatypes other than strings is impossible with
      the key-value pair arrangement.

The Entity-Attribute-Value Model
--------------------------------

The problems we were encountering with the CKAN_ network appear
because in a decentralised environment the equivalence of conceptual
model and SQL table (or group of tables) starts to break down. 
Each node in the network has a slightly different idea of what the
meaning of a model is and supporting these overlapping but different
conceptions is not something that SQL is well suited to.

This is, however, not a new problem. A common problem domain
example is a system to model medical patients' complaints. There are
a large number of possible complaints and any patient will only have
a small number of them. It quickly becomes unwieldy to either have
a very large number of tables, one for each type of complaint (not
to mention what happens when a new complaint is encountered) or to
have a table of patients with a very large number of mostly empty
columns.

If you think of a matrix where the rows correspond to patients and
the columns correspond to complaints, and a particular cell holds
the value 1 if a particular complaint is present for that patient
and 0 otherwise, the matrix will hold mostly zeros. This is known as
a `sparse matrix`_ and is well studied in the mathematical and computer
science literature.

Quite clearly in the CKAN_ problem domain the model is not nearly
as sparse as in the example. In fact most datasets in the catalogue
can be expected to have most of the attributes and the sparse area
is more or less limited to the key-value pair site extensions. However
the more sites there are the larger this subset of metadata becomes.

In data-modelling a model that has these characteristics is known
as an `Entity Attribute Value`_ or EAV_ model. RDF_ is an example of
a way to represent things in an EAV_ manner.

Information Interchange and RDF
-------------------------------

A related problem that arises when we start allowing local extensions
to the data model is about what to do when aggregating data. A simple
answer is to just aggregate the core information but this is very
probably not good enough. What happens when different sites define an
extension with the same name but different meanings?

This is what led us to the `Resource Description Framework`_. In the
RDF_ model, the attributes of an entity (called predicate and subject,
respectively, in the RDF_ nomenclature) are URI_ s. This gives us a 
global namespace that is locally extensible to avoid collisions. 

Furthermore, there are a large variety of existing `RDF Vocabularies`_
which may be useful for describing our data without having to re-invent
the wheel.

It also quickly became apparent that it should be possible to build a
system that can be repurposed for other projects easily - after all if
we are not constrained to put the bulk of our thinking into a SQL 
schema rigidly tied to python classes, then the software becomes more
decoupled from the data and hence more reuseable.

In April of 2010 we started work on a new project with the University
of Edinburgh IDEALab_ for a new type of bibliographic information 
creation and collaboration platform and decided that this was a good
opportunity to pursue this new strategy.

.. _rdf-back-end-design:

RDF back-end Design
-------------------

Some project members had done work with RDF_ before, and we embarked 
on a project to see how the state of the art had advanced since we 
last looked. It was not exceptionally impressive. Without naming names,
the choices for storing RDF data all have several of the following
problems:

    * slow when holding a lot of data
    * large in terms of resource (disc, memory, software) requirements
    * complicated to set-up
    * poor support for aggregate operations
    * poor support for indices on specific values
    * poor support for full-text indices

After some initial efforts using 4store_ we found that a collegue at
the University of Oxford, `Ben O'Steen`_ had been thinking about this
very problem. While the ORDF software only uses some of his lower-level
primitives, the arrangement of the RDF_ storage is very much bears the
mark of his thinking.

The basic idea is to use a variety of indices. The most basic (and most
important) is simply the filesystem. Serialised RDF_ files are stored
in a specialised directory hierarchy. They can be read and written very
quickly and efficiently if you know their identifiers or filenames but
they cannot be searched.

For searching or querying we use two other indices at the moment. We
have persevered with 4store_. This gives us the abilty to search and
explore relationships between entities using the SPARQL_ query language.
We also use Xapian_ for full-text indexing. The actual process of building
the full-text index is somewhat application specific if it is to be done
in a more advanced way than simply looking at some of the predicates 
that commonly contain informative string literals, but that means
that applications using the ORDF software simply need to define one 
function to do this and a corresponding function for searching.

Message Passing
---------------

Once we were committed to having a primary filesystem store and a variety
of associated indices, perhaps allowing indices to exist on different
hosts for scalability, the question arises of how to keep them in sync
and updated.

We use a strategy where a save operation on an RDF_ graph (a named
collection of statements) first writes the new graph into the filesystem
storage and then passes it on to a message queueing system -- RabbitMQ_
in particular. Each index then has a small daemon that then listens for
incoming messages and does whatever updates are required.

This is implemented in such a way as to not *require* the use of RabbitMQ_,
it is perfectly possible to simply iterate over the indexes and give them
the graph to update instead of passing them to the messaging subsystem but
a live, production system would typically make use of the greater
robustness of such a setup.

Use of a message queueing system in this way also opens the way to doing
more expensive operations on the graph after a user may have saved it but
before the indices are updated. A good example would be `Production Rule`_ 
inferencing using, for example, FuXi_ to populate the system with extra
statements that are implied by the data received from the user but not 
explicitly stated. This means richer data and more interesting searching
possibilities. The whole arrangement can start looking like an
`Expert System`_ though there is much to be done first before this
tantalising direction can be fully explored.

Revision Histories and Change Sets
----------------------------------

Another requirement common to most data management projects, CKAN_ and 
Bibliographica_ alike is the keeping of change history data. It is not
simply enough to overwrite previous versions. CKAN_ uses a specially 
implemented `Versioned Domain Model`_ which implements this for objects
in a SQL database.

We decide to build on the Changesets_ vocabulary from Talis. We had to
extend it in a few ways in order to include a notion of RDF_ graphs which
are the basic unit of storage in our back-end and simultaneous changes
to multiple such graphs.

.. _CKAN: http://ckan.net/
.. _Pylons: http://pylonshq.com/
.. _MVC: http://en.wikipedia.org/wiki/Model_View_Controller
.. _Django: http://www.djangoproject.com/
.. _Ruby on Rails: http://rubyonrails.org/
.. _INSPIRE Directive: http://inspire.jrc.ec.europa.eu/
.. _PostGIS: http://www.postgis.org/
.. _GIS: http://en.wikipedia.org/wiki/Geographic_Information_System
.. _PostgreSQL: http://www.postgresql.org/
.. _sparse matrix: http://en.wikipedia.org/wiki/Sparse_matrix
.. _Entity Attribute Value: http://en.wikipedia.org/wiki/Entity-attribute-value_model
.. _EAV: http://en.wikipedia.org/wiki/Entity-attribute-value_model
.. _Resource Description Framework: http://en.wikipedia.org/wiki/Resource_Description_Framework
.. _RDF: http://en.wikipedia.org/wiki/Resource_Description_Framework
.. _URI: http://en.wikipedia.org/wiki/Uniform_Resource_Identifier
.. _RDF Vocabularies: http://esw.w3.org/TaskForces/CommunityProjects/LinkingOpenData/CommonVocabularies
.. _Bibliographica: http://bibliographica.org/
.. _IDEALab: http://idea.ed.ac.uk/
.. _4store: http://4store.org/
.. _Ben O'Steen: http://brii.ouls.ox.ac.uk/about-us/ben-osteen
.. _SPARQL: http://en.wikipedia.org/wiki/SPARQL
.. _Xapian: http://xapian.org/
.. _RabbitMQ: http://www.rabbitmq.com/
.. _Production Rule: http://en.wikipedia.org/wiki/Production_rule
.. _FuXi: http://code.google.com/p/fuxi
.. _Expert System: http://en.wikipedia.org/wiki/Expert_system
.. _Versioned Domain Model: http://www.okfn.org/vdm/
.. _Changesets: http://n2.talis.com/wiki/Changesets
