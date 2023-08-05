__all__ = ["Aggregation"]

from ordf.graph import ConjunctiveGraph
from ordf.namespace import RDF, ORE
from ordf.utils import get_identifier

class Aggregation(ConjunctiveGraph):
    """
    This flavour of :class:`ConjunctiveGraph` exposes aggregations
    as defined by the openarchives ORE vocabulary.
    """
    def __init__(self, store="IOMemory", identifier=None):
        super(Aggregation, self).__init__(store=store)
        self.aggregate = identifier
        if not self:
            self.add((self.identifier, RDF["type"], ORE["Aggregation"]))
        else:
            is_aggregate = False
            for s,p,o in self.triples((self.aggregate, RDF["type"], ORE["Aggregation"])):
                is_aggregate = True
                break
            assert is_aggregate

    def aggregate(self, graph):
        self.add((self.identifier, ORE["aggregates"], graph.identifier))
        graph.add((graph.identifier, ORE["isAggregatedBy"], self.identifier))
        
    def contexts(self):
        for s,p,o in self.triples((self.aggregate, ORE["aggregates"], None)):
            yield Graph(store=self.store, identifier=o)
