Graphs in RDF
=============

In RDF, the notion of what constitutes a graph is not well defined. It is
somewhat analogous to a *document* when thought of as "the collection of
triples obtained by dereferencing the document's URI, but not all graphs
may be obtained in that way. For example, the result of a *CONSTRUCT* or
*DESCRIBE* SPARQL query typically returns an unnamed graph. In N3
inferencing rules, such as::

    { ?x a Cat } => { ?x a Animal } .

both the left and right hand sides of the rules are themselves embedded
or "quoted" graphs.

Some of our initial reasons for considering how to talk about graphs are
discussed in the :ref:`changesets` section of this manual.

The *rdfg* vocabulary gives us some concepts for talking about graphs.
It is very small, so quoted in its entirety below::

    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix rdfg: <http://www.w3.org/2004/03/trix/rdfg-1/> .

    rdfg:Graph a rdfs:Class ;
        rdfs:label "Graph" ;
	rdfs:comment "An RDF graph (with intensional semantics)." .

    rdfg:equivalentGraph a rdf:Property ;
        rdfs:label "equivalent graph" ;
	rdfs:comment "The graphs associated with the subject and object are
		      equivalent." ;
	rdfs:domain rdfg:Graph ;
	rdfs:range rdfg:Graph .

    rdfg:subGraphOf a rdf:Property ;
        rdfs:label "subgraph of" ;
	rdfs:comment "The graph associated with the subject is a subgraph of
		      a graphequivalent to that associated with the object." ;
	rdfs:domain rdfg:Graph ;
	rdfs:range rdfg:Graph .

This is useful as far as it goes, but there seem to be two problems with
it. First it is a completely closed vocabulary, that is there is a class and
two predicates for talking about that class but no way of referring to the
class as such from outside. Second, and this is likely intentional on the
part of the authors, there is no inverse of *rdfg:subGraphOf*.

To tackle the first problem (in the context of :ref:`changesets`) we define::

    @prefix ordf: <http://purl.org/NET/ordf/> .

    ordf:graph a rdf:Property ;
        rdfs:range rdfg:Graph ;
        rdfs:label "graph" ;
        rdfs:comment "Reference to a graph" .

The second problem is harder and what we are trying to accomplished is best
explained with reference to `Bibliographica`_ a website built with 
`openbiblio`_ a `Pylons`_ application that uses ORDF. Without going into
the intricacies of conceptual frameworks for organisation of libraries, we
have two fundamental entities that we're concerned with: People (authors,
translators, publishers, etc.) and Works (books, musical scores, recordings,
etc.).

We have chosen that each individual entity merits its own URI, its own Graph
in the system. So each Work, each Person has a page with some statements 
about them.

Now users of the system are going to want to see, most often, not just
biographical information about a Person but the list of works (with some
metadata) that they are responsible for. Or they will want to see complete
information about a work together with abbreviated information about the
authors and publishers.

Because we allow editing of the data in a *wikiesque* way, it is very
important that we keep straight where any triples being added or modified
belong, and the best way to do this is to ensure that they only exist in
one place. 

So need a way to specify the construction of conjunctive graphs, to use
the terminology from `RDFLib`_. But we don't want to explicitly construct
them, we want the client to take care of that.

So we might have something like this::

    DostoyevskyAndWorks a rdfg:Graph ;
        ordf:subGraph Dostoyevsky ;
        ordf:subGraph CrimeAndPunishment ;
        ordf:subGraph TheIdiot .


and the client would see this and look at all the *ordf:subGraph* triples
and then pull them in by reference. Of course we have to define this
predicate::

    ordf:subGraph a rdf:Property ;
        rdfs:label "sub-graph" ;
        rdfs:comment "Indicates a sub-graph containing statements belonging
		      also to this rdfg:Graph" ;
        rdfs:domain rdfg:Graph ;
        rdfs:range rdfg:Graph .


Note that it is not possible (or desirable in our application) to write 
the inference rule, "If S is a sub-graph of G --> all statements in S
are also in G".

This also brings up an interesting way of handling which :ref:`fresnel-lenses`
are intended to be used to view a resource. Noticing the lack of a general
predicate for referring to lenses, we define *ordf:lens*, and apply it
in our conjunctive graph::

    ordf:lens a rdf:Property ;
        rdfs:label "lens" ;
        rdfs:comment "Which Fresnel lens to use when displaying this graph" ;
        rdfs:domain rdfg:Graph ;
        rdfs:range fresnel:Lens .

    DostoyevskyAndWorks ordf:lens AuthorAndWorksLens .

In the case of specialised aggregate graphs it would even be quite
possible to define the lens directly therein.

.. _Bibliographica: http://bibliographica.org/
.. _openbiblio: http://knowledgeforge.net/pdw/openbiblio
.. _Pylons: http://pylonshq.com/
.. _RDFLib: http://www.rdflib.net/