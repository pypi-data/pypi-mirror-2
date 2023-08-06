.. _changesets:

Change Sets
===========

Changesets are implemented using an extension of the `RDF ChangeSet Vocabulary`_. 
There is a good overview of the subject as it originally stood on the 
`Talis wiki page`_. The changeset vocabulary as defined by Talis has some 
limitations, unfortunately. In particular,

 * a changeset is limited to statements about a single subject
 * there is no way to specify which *graph* that the changes pertain to

The second problem is more a limitation of RDF itself as originally specified 
though there has been talk of fixing this in the next version.

An example changeset that keeps to the original spec might look something like
this::

    :csid a cs:ChangeSet ;
        cs:createdDate "1970-01-01"^^xsd:date ;
	cs:creatorName "Some Body" ;
	cs:changeReason "A change must be made" ;
	cs:preceedingChangeSet :previousid ;
	cs:subjectOfChange <http://example.org/> ;
	cs:addition [
	    rdf:subject <http://example.org/> ;
	    rdf:predicate rdfs:label ;
	    rdf:object "Example"
	] .

In otherwords, add a label to *http://example.org/*. There is a corresponding
predicate, *cs:removal* to remove statements. The linkage with *cs:preceedingChangeSet*
points to the previous change involving that resource which gives a way to walk
the change history.

It is not clear why there can only be one *cs:subjectOfChange* and that every
*cs:addition* and *cs:removal* must concern only it. Most often changes that are
made will concern more than one resource and it is natural to consider them together
as a single atomic unit.

**The first extension** that we have implemented is to allow multiple 
*cs:subjectOfChange* values and remove the restriction on the resources that
are added or removed.

In our implementation, though this is not true of RDF generally, we have a quite
clear notion of what constitutes an *RDF graph*. Namely it is a collection of
triples. It might easily correspond to the notion of a document because it is the
collection of triples that you receive when dereferencing a particular URI (i.e.
the *identifier* of that graph). When we make changes, we don't make changes to
triples in the abstract sense, rather we make changes to the triples that exist
in a particular graph.

This does not require changes to the range of *cs:subjectOfChange* since its 
range is *rdfs:Resource*, and from the specification,

      All things described by RDF are called resources, and are instances 
      of the class rdfs:Resource. This is the class of everything.

That said, the range could be narrowed if there were such an entity as *rdf:Graph*
though the utility of such a class is debatable.

What *is* required is for a way to specify the graph concerned in the reified 
triples. What we really want to do is::

	cs:addition [
	    rdf:subject <http://example.org/> ;
	    rdf:predicate rdfs:label ;
	    rdf:object "Example" ;
	    rdf:graph <http://example.org/data/>
	] .

but we are prevented through lack of a suitable *rdf:graph* predicate. (n.b.
there is no reason why the objects of *rdf:subject* and *rdf:graph* could not
be the same, in fact in most instances they probably would be).

**The second extension** is the definition of a predicate for use in reification
to indicate the graph in question. The predicate is, for the time being::

	 http://bibliographica.org/schema/graph#graph

though we are hopeful a suitable replacement will be included in RDF in the
future and, failing that, we will try to obtain a http://purl.org namespace for
it.

We also require a way to indicate which changeset is the most recent for a 
particular graph and so we add a triple::

	   :graphid ordf:changeSet :csid

to graphs so modified.

**The third extension** is to introduce a property *ordf:changeSet* into the
changeset vocabulary for referring to instances of the *cs:ChangeSet* class.

**The fourth extension** is not so much concerned with structure so much as
summarising information about a changeset. We introduce *ordf:additionCount* 
and *ordf:removalCount* to be the number of additions and removals in a 
particular changeset.

.. automodule:: ordf.vocab.changeset

.. _RDF ChangeSet Vocabulary: http://purl.org/vocab/changeset
.. _Talis wiki page: http://n2.talis.com/wiki/Constructing_a_Changeset