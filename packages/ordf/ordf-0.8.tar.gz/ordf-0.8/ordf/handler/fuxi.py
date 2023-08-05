"""
.. autoclass:: FuXiReasoner
   :show-inheritance:
"""

from ordf.graph import Graph, _Graph, ConjunctiveGraph
from ordf.handler import Handler, HandlerPlugin
from ordf.namespace import CS, RDF
from ordf.term import URIRef

from FuXi.Rete.RuleStore import SetupRuleStore
from FuXi.Horn.HornRules import HornFromN3
from FuXi.Rete.Util import generateTokenSet
from FuXi.Syntax.InfixOWL import Class, Property
from StringIO import StringIO
from getpass import getuser
from string import strip

from logging import getLogger
log = getLogger(__name__)

class FuXiReasoner(HandlerPlugin):
    """
    This handler implements a production rule reasoning system. In
    normal operation it would listen to a one queue using
    :class:`~ordf.handler.queue.RabbitHandler` and the handler would
    be configured to write to a different exchange using
    :class:`~ordf.handler.queue.RabbitQueue`.

    When the :meth:put method is called, it will be with a store that
    already contains a :class:`~ordf.changeset.ChangeSet`. This handler
    reasons over all of the non-changeset graphs in the store using the
    rules and for whatever statements it is able to infer adds them to
    the graphs and creates a new, (incremental) changeset.

    The resulting store is then passed back up to the handler where
    it should go out the outbound handlers and eventually be indexed.

    The configuration for this is slightly subtle, see the
    :ref:`configuring-inferencing` section of the configuration guide
    for how to do this.

    :param rule_modules: comma separated list of modules that export
        an :meth:`inference_rules` method
    """
    def __init__(self, rule_modules, **kw):
        super(HandlerPlugin, self).__init__(**kw)
        self.rule_modules = map(strip, rule_modules.split(","))
        self.busy = False

    def put(self, store):
        if self.busy:
            return
        self.busy = True

        if isinstance(store, _Graph):
            store = store.store

        def _get(graph):
            if isinstance(graph, basestring):
                identifier = graph
            else:
                identifier = graph.identifier
            for ctx in store.contexts():
                if ctx.identifier == identifier:
                    return ctx
        self.get = _get

        rstore, rgraph, rete = SetupRuleStore(makeNetwork=True)
        rete.inferredFacts = Graph()
        for modname in self.rule_modules:
            __import__(modname, {}, {}, ["inference_rules"]).inference_rules(self.handler, rete)

        ### widen the set of statements to inference from
        ### any references, at one degree from the contents of
        ### the store, to external resources, add them to the
        ### store
        for s,p,o in ConjunctiveGraph(store).triples((None, None, None)):
            if isinstance(o, URIRef):
                o_graph = self.get(o)
                if not o_graph:
                    continue
                o_graph_copy = Graph(store=store, identifier=o_graph.identifier)
                for statement in o_graph.triples((None, None, None)):
                    o_graph_copy.add(statement)

        ### we don't reason on changesets, so make a list of changesets we have
        changesets = []
        for ctx in store.contexts():
            for statement in ctx.triples((ctx.identifier, RDF.type, CS.ChangeSet)):
		log.debug("skip %s" % ctx.identifier)
                changesets.append(ctx.identifier)
                break

        ### feed data to the reasoner
        for ctx in store.contexts():
            if ctx.identifier in changesets:
                continue
            log.debug("facts %s" % ctx.identifier)
            rete.feedFactsToAdd(generateTokenSet(ctx))

        ### construct the change context
        change_ctx = self.handler.context(getuser(), "FuXi machine reasoning")
        for ctx in store.contexts():
            if ctx.identifier in changesets:
                ### if a previous changeset, just preserve it in the change context
                ### store
                copy = Graph(store=change_ctx.store, identifier=ctx.identifier)
                for statement in ctx.triples((None, None, None)):
                    copy.add(statement)
            else:
                ### otherwise, add the relevant inferred facts
                ### this is a naive way of figuring out which inferred
                ### facts are relevant
                copy = Graph(identifier=ctx.identifier)
                copy += ctx
                copy += rete.inferredFacts.bnc((ctx.identifier, None, None))
                change_ctx.add(copy)

        ### save the changes
        ### this doesn't loop back through this function because
        ### at this point self.busy == True
        cs = change_ctx.commit()
        ### if we haven't been able to make any inferences, this changeset
        ### will be empty. but the preceding changeset will not, so we
        ### still need to send it to the indices
        if not cs:
            self.handler.put(change_ctx.store)

        ### get ready for the next message
        self.get = lambda x: None
        self.busy = False

        ### prevent further propagation of the original change bundle
        return True
