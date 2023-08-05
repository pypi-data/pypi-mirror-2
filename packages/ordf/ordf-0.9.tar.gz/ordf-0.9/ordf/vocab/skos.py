from ordf.graph import Graph
from logging import getLogger

log = getLogger(__name__)
skos_rdf = "http://www.w3.org/TR/skos-reference/skos.rdf"

def rdf_data():
    log.info("Fetching %s" % skos_rdf)
    g = Graph(identifier=skos_rdf).parse(skos_rdf)
    log.info("Parsed %s (%d triples)" % (skos_rdf, len(g)))
    yield g

def inference_rules(handler, network):
    from FuXi.DLP.DLNormalization import NormalFormReduction
    skos = handler.get(skos_rdf)
    if len(skos) == 0:
        for skos in rdf_data():
            handler.put(skos)
    NormalFormReduction(skos)
    return network.setupDescriptionLogicProgramming(skos, addPDSemantics=False)
