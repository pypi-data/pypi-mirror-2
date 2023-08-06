
Layercake RDFLib with ORDF
==========================

Layercake is a branch of rdflib used at the Cleveland Clinic
with FuXi. Amongst other things it has some support for remote
SPARQL stores (relevant to `ticket 105`_). Some additional
information is available from the `wiki page explaining layercake`_
and the `layercake message on FuXi discuss`_.

.. _ticket 105: http://knowledgeforge.net/pdw/trac/ticket/105
.. _wiki page explaining layercake: http://code.google.com/p/python-dlp/wiki/LayerCakePythonDivergence
.. _layercake message on FuXi discuss: http://groups.google.com/group/fuxi-discussion/msg/d9f3be240efb81ab

Installation recipe
-------------------

Before following the usual install procedure, do::

    pip install pyparsing
    pip install -e svn+http://python-dlp.googlecode.com/svn/trunk/layercake-python#egg=rdflib

And then for example,::

    pip install hg+https://fuxi.googlecode.com/hg/#egg=fuxi
    pip install -e hg+http://ordf.org/src/#egg=ordf
    pip instlal -e hg+http://ordf.org/src/ontosrv/#egg=ontosrv
