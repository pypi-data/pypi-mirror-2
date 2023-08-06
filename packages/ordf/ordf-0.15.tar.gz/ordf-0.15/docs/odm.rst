Object Description Mapper
=========================

When working with SQL databases, it is common to use what is known as an
Object-Relational Mapper that gives you constructs in a high level 
object-oriented language that persist their data in a relational
database. By analogy, in ORDF we have an *Object Description Mapper*.
This bears a little explaining.

Information is structured in RDF in terms of triples. Higher level
constructs are built on top of these using various vocabularies,
the most basic of which being `RDFS`_. RDFS provides basic things
like a way to specify domain and range restrictions on predicates
and a way to construct a class hierarchy. `OWL` build upon RDFS
and provides ways to express more complex relationships between
classes.

The previous state of the art in ORM-like things for RDF tries to
model things at the basic RDF level, with no particular support for
RDFS or OWL. Also common is a disregard for handling of *graphs*
which, as an otherwise unconstrained container for triples has no
analogue in the RDBMS world.

Building upon a modified version of `InfixOWL`_, ORDF tries to 
bridge this gap. Because that which is expressed by OWL has the
characer of a `Description Logic`_, the result is called an
*Object Description Mapper*. It provides constructs that will 
seem familiar to those used to ORMs like `SQLAlchemy`_ or
`Django`_ but which are backed by an RDF store containing multiple
graphs and are ultimately expressed in OWL.

Individuals
-----------

The basic building blocks are contained in the :mod:`ordf.vocab.owl`
module. A typical pattern is to declare a subclass of
:class:`ordf.vocab.owl.AnnotatibleTerms` and set some properties on it using
convenience methods. For example:

.. code-block:: python


   ## preamble
   from ordf.namespace import register_ns, Namespace
   register_ns("data", Namespace("http://example.org/data#"))
   register_ns("ont", Namespace("http://example.org/ontology#"))

   ## imports required for the example   
   from ordf.namespace import DATA, ONT, FOAF
   from ordf.term import URIRef
   from ordf.vocab.owl import AnnotatibleTerms, predicate

   ## define a python class for individuals of type FOAF.Person
   class Person(AnnotatibleTerms):
       def __init__(self, *av, **kw):
           super(Person, self).__init__(*av, **kw)
	   self.type = FOAF.Person
       name = predicate(FOAF.name)
       homepage = predicate(FOAF.homepage)

   ## create a person
   bob = Person(DATA.bob)
   bob.name = "Bob"
   bob.homepage = URIRef("http://example.org/")

   ## see what the RDF looks like
   print bob.graph.serialize(format="n3")

As might be expected, the result of doing this is a graph like the 
following::

    @prefix data: <http://example.org/data#>.
    @prefix foaf: <http://xmlns.com/foaf/0.1/>.
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.

    data:bob a foaf:Person;
        foaf:homepage <http://example.org/>;
        foaf:name "Bob". 

This is not so different from your standard ORM. However we haven't seen
persistence yet. The *Person()* constructor will take an optional (but
recommended) argument called *graph*. You need to specify this to say
where the information should be stored. By default a transient in-memory
graph is created if none is specified, but something a bit more realistic
might be:

.. code-block:: python

   from ordf.graph import Graph
   from rdflib.store.Sleepycat import Sleepycat

   store = Sleepycat("/tmp/test_db")
   graph = Graph(store, identifier="http://example.org/bob.rdf")
   bob = Person(DATA.bob, graph=graph)
   ... as above

Now any statements that are made about *bob* will be persisted in the
specified store so that next time, we just have to initialise the store
and construct the *bob* instance of *Person* and all the data will be
there.

Notice the use of :class:`ordf.vocab.owl.predicate` to assign class
variables. It is one of a family of classes. In total we have:

    * :class:`ordf.vocab.owl.predicate` a simple predicate whose
      object may be any kind of term.
    * :class:`ordf.vocab.owl.cached_predicate` same as above but
      the results of getting the value are cached.
    * :class:`ordf.vocab.owl.object_predicate` a predicate whose
      object is another individual.
    * :class:`ordf.vocab.owl.cached_object_predicate` same as
      above but with caching.

The use of :class:`ordf.vocab.owl.object_predicate` makes relations
that are analogous to foreign keys in a SQL ORM. Here's an example.

.. code-block:: python

    from ordf.graph import Graph
    from ordf.vocab.owl import AnnotatibleTerms, object_predicate

    class Country(AnnotatibleTerms):
        def __init__(self, *av, **kw):
            super(Country, self).__init__(*av, **kw)
            self.type = ONT.Country

    class City(AnnotatibleTerms):
    	def __init__(self, *av, **kw):
	    super(City, self).__init__(*av, **kw)
	    self.type = ONT.City
	country = object_predicate(ONT.country, Country)

    data = Graph()

    scotland = Country(DATA.scotland, graph=data)
    scotland.label = "Scotland"

    edinburgh = City(DATA.edinburgh, graph=data)
    edinburgh.label = "Edinburgh"
    edinburgh.country = scotland

    for country in edinburgh.country:
        print type(country), [str(x) for x in country.label]

output::

    <class 'Country'> ['Scotland']

Two things are important to note here. When you access a instance property that
has been made with one of the *predicate* classes, you always get a generator
or list back. This is because there is no way to know how many objects have
been assigned with the predicate in question. That's just the way it is with
RDF. The *Subject, Predicate, Object* model can always be thought of as
*Entity, Attribute, list of Values*.

The second thing to note is that we have said nothing about the nature of
the OWL classes that we are dealing with nor about the predicates. Nowhere
have we written down anything about the domains and ranges involved or 
other restrictions or class hierarchy. There is no description logic 
embedded in these examples so far. The next section talks more about this.

Classes in OWL
--------------

The main purpose of `InfixOWL`_ is to express a `Description Logic`_, the 
relationships between OWL classes and the nature of the predicates in 
question. There is a bit of a nomenclature collision here. The word *class*
is used both in python and in OWL to refer to a concept that, though it
is related, is for practical purposes quite different. In particular, we
can define a python class, using :class:`ordf.vocab.owl.Class` but to 
create the OWL class, we need to instantiate it. We need to instantiate
it because instantiating it means putting triples in a graph, and there
is no such graph available at the time the python class is made. Sure we
could do some magic with metaclasses, but it is probably best to keep 
things simple and keep the magic out of it.

Continuing on from the previous example, where we created some individuals
that are part of the OWL classes *ont:Country* and *ont:City*, we can start
defining our ontology:

.. code-block:: python

    from ordf.vocab.owl import Class

    class PlaceClass(Class):
        def __init__(self, **kw):
	    super(PlaceClass, self).__init__(ONT.Place, **kw)

    class CountryClass(Class):
        def __init__(self, **kw):
	    super(CountryClass, self).__init__(ONT.Country, **kw)
	    self.subClassOf = PlaceClass(graph=self.graph)
	    self.factoryClass = Country
	    self.label = "Country"

    class CityClass(Class):
        def __init__(self, **kw):
	    super(CityClass, self).__init__(ONT.City, **kw)
	    self.subClassOf = PlaceClass(graph=self.graph)
	    self.factoryClass = City
	    self.label = "City"

    ontology = Graph()

    country = CountryClass(graph=ontology, factoryGraph=data)
    city = CityClass(graph=ontology, factoryGraph=data)

    print [str(x) for x in country.get(DATA.scotland).label]

A common convention is to separate out the ontology and the concrete individuals
into separate graphs. For this reason there is a settable instance attribute (or
keyword argument to the constructor) on instances of :class:`ordf.vocab.owl.Class`
called *factoryGraph*.

Instances of :class:`ordf.vocab.owl.Class` have methods called *get* and
*get_or_create* that are used as simple ways of obtaining individuals of that
class from the factory graph.

At this stage we have two graphs containing data that looks like this.

The ontology graph::

    @prefix ont: <http://example.org/ontology#>.
    @prefix owl: <http://www.w3.org/2002/07/owl#>.
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.

    ont:City a owl:Class;
        rdfs:label "City";
        rdfs:subClassOf ont:Place. 

    ont:Country a owl:Class;
        rdfs:label "Country";
        rdfs:subClassOf ont:Place. 

    ont:Place a owl:Class. 

The data graph::

    @prefix data: <http://example.org/data#>.
    @prefix ont: <http://example.org/ontology#>.
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.

    data:edinburgh a ont:City;
        rdfs:label "Edinburgh";
        ont:country data:scotland. 

    data:scotland a ont:Country;
        rdfs:label "Scotland". 

Queries and Filters
-------------------

Let's add another country to the data graph,

.. code-block:: python

    russia = Country(DATA.russia, graph=data)
    russia.label = "Russia"

We've seen how the :meth:`ordf.vocab.owl.Class.get` method works, but what if
we want to retrieve something where we don't know the subject URI? We can
do this if we have `Telescope`_ installed. Unfortunately this only works at
the moment with older (2.4.X) rdflib.

.. code-block:: python

    from ordf.namespace import RDFS
    from ordf.term import Literal
    from telescope import v

    for c in country.filter((v.id, RDFS.label, Literal("Russia"))):
        print [str(x) for x in c.label]

If you would rather have the SPARQL query that is used to select individuals
by identifier, you can use the :meth:`ordf.vocab.owl.Class.query` method
instead of :meth:`ordf.vocab.owl.Class.filter`:

.. code-block:: python

   q = country.query((v.id, RDFS.label, Literal("Russia")))
   print q.compile()

will produce output like::
          
    SELECT DISTINCT ?id
    WHERE {
        ?id <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://example.org/> . 
        ?id <http://www.w3.org/2000/01/rdf-schema#label> "Russia" 
    }

Being able to access the query directly is useful if you are working with
a back-end triple store (e.g. `4store`_) that might be able to process SPARQL
queries faster than going through RDFLib. You can then do something like,

.. code-block:: python

   from py4s import FourStore
   from ordf.graph import ConjunctiveGraph

   store = FourStore("somekb,soft_limit=-1")
   data = ConjunctiveGraph(store)

   country = CountryClass(graph=ontology, factoryGraph=data)

   q = country.query((v.id, RDFS.label, Literal("Russia")))
   results = [country.get(ident)
              for ident, in store.query(q.compile())]

This is particularly helpful for complex queries involving unions or large
potential result sets where processing the *DISTINCT* operator with RDFLib
might be prohibitively expensive.


Description Logic
-----------------

Given the definitions above, we might expect that we can find places in a
generic way but unfortunately,

.. code-block:: python

   >>> places = PlaceClass(graph=ontology, factoryGraph=data)
   >>> places.get(DATA.edinburgh)
   Traceback (most recent call last):
     raise KeyError("no individual %s with type %s" % (identifier, self.identifier))
   KeyError: u'no individual http://example.org/edinburgh with type http://example.org/Place'

With a little bit of preparation, however, this can be made to work. There
are two strategies for doing this. The first, and simplest, is called
forward chaining. What this means is that all facts that can be inferred
from the ontology and data are added to the data graph:

.. code-block:: python

    from FuXi.Rete.RuleStore import SetupRuleStore
    from FuXi.Rete.Util import generateTokenSet

    rule_store, rule_graph, network = SetupRuleStore(makeNetwork=True)
    network.reset(data)
    network.setupDescriptionLogicProgramming(ontology)
    network.feedFactsToAdd(generateTokenSet(data))

    assert places.get(DATA.scotland) == scotland
    assert places.get(DATA.edinburgh) == edinburgh

Mind that this inferencing step can be processor intensive as well as
data intensive if the ontology is complex and there are lots of facts that
can be inferred.

The call to *network.reset()* causes the Rete network to add inferred
facts to the data graph. the *setupDescriptionLogicProgramming* transforms
the ontology into Horn rules and the *feedFactsToAdd* passes all of the 
known facts that exist in the data graph through the network. The result
is that *data* now contains::

    @prefix data: <http://example.org/data#>.
    @prefix ont: <http://example.org/ontology#>.
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.

    data:edinburgh a ont:City,
            ont:Place;
        rdfs:label "Edinburgh";
        ont:country data:scotland. 

    data:scotland a ont:Country,
            ont:Place;
        rdfs:label "Scotland". 

    data:russia a ont:Country,
            ont:Place;
        rdfs:label "Russia".

The second strategy is backward chaining and is a little more complex to
set up. The advantage is that any required facts that are not explicitly
in the data graph are computed on the fly so don't take up extra disk 
space, and also that the required facts are dependent on the query so
irrelevant facts won't be deduced. The disadvantage is greater CPU overhead
at query time, and the aforementioned complexity with setting it up.

*... To be continued*

.. _RDFS: http://www.w3.org/TR/rdf-schema/
.. _OWL: http://www.w3.org/TR/owl-overview/
.. _InfixOWL: http://code.google.com/p/fuxi/wiki/InfixOwl
.. _Description Logic: http://en.wikipedia.org/wiki/Description_logic
.. _SQLAlchemy: http://www.sqlalchemy.org/
.. _Django: http://www.djangoproject.com/
.. _Telescope: https://bitbucket.org/exogen/telescope
.. _4store: http://4store.org/
