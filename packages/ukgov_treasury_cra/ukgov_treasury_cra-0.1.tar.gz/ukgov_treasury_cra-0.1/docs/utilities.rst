Command Line Utilities
======================

There is only one command-line utility at the present stage, :program:`cra2009`
that loads the 2009 version of the CRA data into an RDF store.

.. _cra2009:

:program:`cra2009`
------------------

This utility is implemented by the :class:`ukgov.hmt.cra.CRA2009` class.

For performance reasons, this doesn't use the handler machinery from
ORDF as such. Rather it looks at the handler object for writers that
provide an RDFLib compatible storage interface and uses these directly.
The supported ones are :class:`ordf.handler.rdf.RDFLib` and 
:class:`ordf.handler.rdf.FourStore` though the latter is recommended
for a full load of the CRA data since it is rather large. There will
be no changesets associated with this loading operation

As a result of this, if you have configured ORDF with multiple storage
back-ends, the data will only exist in one. To push the data to the
other indices, you will have to run the :program:`ordf` command with
the '--reindex' option specifying the triplestore with `--readers`
and any other index with `--writers`.

*insert more documentation and usage examples here*