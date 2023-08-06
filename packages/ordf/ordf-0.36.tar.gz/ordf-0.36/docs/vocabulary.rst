RDF Graphs
==========

.. automodule:: ordf.graph

Vocabulary Modules
==================

Various RDF vocabularies benefit from specific support in Python. They
are implemented as sublcasses of :class:`ordf.graph.Graph`.

As well, this is a place to put data and rule fixtures for loading with
:program:`ordf_load`. The functions that should be implemented,
:func:`rdf_data` and :func:`inference_rules`. The former takes no
arguments and should return an iterable of graphs to be added to the
store. The latter takes two arguments, *handler* and *network* where
*network* is an instance of :class:`FuXi.Rete.Network.ReteNetwork`
and its job is to populate the network with inference rules.

Fixture Examples
----------------

An :func:`rdf_data` implementation that reads N3 files bundled with
the distribution:

.. code-block:: python

    from ordf.graph import Graph
    import os, pkg_resources

    def rdf_data():
	graph = Graph(identifier="http://example.org/schema")
	fp = pkg_resources.resource_stream("example.vocab",
	                                   os.path.join("n3", "example.n3"))
	graph.parse(fp, format="n3")
	fp.close()
	yield graph

An :func:`rdf_data` implementation that retrieves a vocabulary from the Internet:

.. code-block:: python

    from ordf.graph import Graph

    def rdf_data():
        graph_uri = "http://purl.org/NET/example/"
	graph = Graph(identifier=graph_uri)
	graph.parse(graph_uri)
	yield graph

Inference rules are slightly more complicated according to whether they
are inferred from description logic (e.g. an *OWL* Ontology) or from 
hand-written rules in N3. Hand-written rules follow a similar pattern as
the first :func:`rdf_data` implementation above:

.. code-block:: python

    import os, pkg_resources

    def inference_rules(handler, network):
        from FuXi.Horn.HornRules import HornFromN3
	rule_file = pkg_resources.resource_filename("example.vocab",
	                                            os.path.join("n3", "example-rules.n3"))
	rules = HornFromN3(rule_file)
	for rule in rules:
	    network.buildNetworkFromClause(rule)
	return rules

In the case of description logic, it is usually a good idea to make sure
the graph exists in the store already, and save it there if it doesn't:

.. code-block:: python

    def inference_rules(handler, network):
        from FuXi.DLP.DLNormalization import NormalFormReduction
	onto = handler.get("http://example.org/ontology")
	if len(onto) == 0:
	    for onto in rdf_data():
	        handler.put(onto)
	NormalFormReduction(onto)
	return network.setupDescriptionLogicProgramming(onto, addPDSemantics=False)

Note that this makes use of :func:`rdf_data` that is assumed to be defined
in the same module and whose job it is to retrieve the ontology graph from
whatever source.

Note also that in both these cases the import from the :mod:`FuXi` package is 
done within the scope of the function. This is so that if inferencing is not
required and :mod:`FuXi` is not installed there will be no :class:`ImportError`
and any :func:`rdf_data` fixtures and concrete implementations will still be
useable.

Concrete Implementations
------------------------

.. toctree:: 
   :maxdepth: 2

   ordf_vocab_changeset
   ordf_vocab_foaf
   ordf_vocab_fresnel
   ordf_vocab_opencyc
   ordf_vocab_opmv
   ordf_vocab_ore
   ordf_vocab_owl