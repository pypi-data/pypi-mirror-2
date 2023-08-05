RDF Notation 3
==============

ORDF processes triples and can read and serialise in most
of the standard representations. However for RDF data that we
write as part of the workings of the system we will almost 
invariably use Notation 3 or N3 because of its clarity and 
expressivity. We typically write RDF by hand when we are 
creating instructions for display of data (corresponding
to the *View* part of a traditional *Model-View-Controller*
paradigm). It also becomes useful when we come to the more
advanced capabilities of inferencing.

.. toctree::
   :maxdepth: 2

W3C Documentation
-----------------

N3 is a standard syntax defined by the W3C. The canonical document
is the `Notation 3 Design Issues`_ article by Tim Berners-Lee. It
however makes for some rather dry reading.

More accessible are the materials from the `Semantic Web Tutorial
Using N3`_ from the WWW2003 conference in Budapest. They progress
step by step from the most verbose and unadorned way of presenting
information through syntactic sugar to present the same in an
easily readable and understandable way. The tutorial goes further
to writing entailment rules -- a special case of `Horn clauses`_
and shows how to use the python program `CWM`_ to use these rules
to draw inferences and make proofs from RDF data.

.. _fresnel-lenses:

Fresnel Lenses
--------------

The main circumstance in which we write RDF by hand using N3 is 
when creating "lenses" to display data using the `Fresnel`_ 
vocabulary. There are some `examples of lenses we have written`_
in the openbiblio mercurial respository.

`Fresnel`_ is a way of writing instructions in RDF for the display
of RDF data. The output is an XHTML fragment, a set of nested 
<div /> elements. The instructions include specifying CSS classes
for styling.

A very simple example, with namespace declarations omitted, suppose
we have the following data,

::

    :alice a foaf:Person ; 
        foaf:name "Alice" ; 
        foaf:homepage <http://example.org/alice> .

    :bob a foaf:Person ; 
        foaf:name "Bob" ; 
        foaf:homepage <http://example.org/bob> .

We can write a very simple lens to display every *foaf:Person* with
all of their properties like so,

::

    :personLens a fresnel:Lens ;
        fresnel:classLensDomain foaf:Person ;
        fresnel:purpose fresnel:DefaultLens ;
        fresnel:showProperties (
            fresnel:allProperties
        ) .

Which results in HTML that looks something like,

::

    <div class="fresnel_container">
        <div class="fresnel_resource">
            <div class="fresnel_property>
                <span class="fresnel_label">name</span>
                <div class="fresnel_value">
                    <div class="fresnel_container">
                        <p>Alice</p>
                    </div>
                </div>
            </div>
            <div class="fresnel_property">
                <span class="fresnel_label">homepage</span>
                <div class="fresnel_value">
                    <div class="fresnel_container">
                        <a href="http://example.org/alice">http://example.org</a>
                    </div>
                </div>
            </div>
        </div>
    </div>

for Alice and likewise for Bob. `Fresnel`_ has a way of adding specific
CSS classes or styling instructions to each of these <div /> elements. It
is possible to hide or substitute alternative labels as well as prepend
or append text.

ORDF contains a `Javascript implementation of Fresnel`_
building upon the `rdfquery`_ plugin for the `jQuery` framework. The 
corresponding Javascript editing interface that we have written also
uses the current lens such that one can add only predicates that the
lens is concerned with.

A python implementation of `Fresnel`_ is planned so as not to depend on
Javascript for rendering HTML representations of RDF graphs.

.. _inference-rules:

Inference Engines
-----------------

Though `CWM`_ was the first RDF inference engine it is now largely
unmaintained and does not use the most efficient techniques of 
producing entailed statements. It is best thought of these days as
a reference implementation, particularly for the N3 language.

The alternative for python is the `FuXi`_ reasoner by `Chimezie
Ogbuji`_ which we are using. It supports both production rule
(generating statements entailed by the rules) and back-chaining
(working from a constraint to find all statements from the data
and rules that satisfy) styles of reasoning and uses the more 
`Rete algorithm`_ for the former -- running much faster than 
`CWM`_.

At present we use only very simple inference rules. This one::

    { ?s a ?t } => { ?s a owl:Thing } .

says that if *?s* has a type, then it should also have the *owl:Thing*
type. This is used to allow the generic OWL lens to work with
most any data.

Another case is enabling good practice by filling in *rdfs:label*
on things. For example::

    { ?s a foaf:Person .
      ?s foaf:name ?n } => { ?s rdfs:label ?n } .

    { ?s a frbr:Work .
      ?s dc:title ?t } => { ?s rdfs:label ?t } .

that is, if *?s* is a person, use their name as label. If *?s*
is a *frbr:Work* use the title.

.. _Notation 3 Design Issues: http://www.w3.org/DesignIssues/Notation3.html
.. _Semantic Web Tutorial Using N3: http://www.w3.org/2000/10/swap/doc/Overview.html
.. _Horn clauses: http://en.wikipedia.org/wiki/Horn_clause
.. _CWM: http://www.w3.org/2000/10/swap/doc/cwm
.. _FuXi: http://code.google.com/p/fuxi/
.. _Chimezie Ogbuji: http://chimezie.posterous.com/
.. _Rete algorithm: http://en.wikipedia.org/wiki/Rete_algorithm
.. _Fresnel: http://www.w3.org/2005/04/fresnel-info/manual/
.. _examples of lenses we have written: http://knowledgeforge.net/pdw/openbiblio/file/tip/openbiblio/lenses/
.. _Javascript implementation of Fresnel: http://knowledgeforge.net/pdw/ordf/file/tip/public/js/jquery.fresnel.js
.. _rdfquery: http://code.google.com/p/rdfquery/
.. _jQuery: http://code.google.com/p/rdfquery/
