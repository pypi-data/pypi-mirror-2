qubic.sphinx.graphvizinclude
============================

Overview
--------

This package defines an extension for the
`Sphinx <http://sphinx.pocool.org>`_ documentation system.  The extension
allows generation of Graphviz from external .dot resources


Installation
------------

Install via `easy_install
<http://peak.telecommunity.com/DevCenter/EasyInstall>`_::

 $ bin/easy_install qubic.sphinx.graphvizinclude

or any other means which gets the package on your ``PYTHONPATH``.


Registering the Extension
-------------------------

Add ``qubic.sphinx.graphvizinclude`` to the ``extensions`` list in the
``conf.py`` of the Sphinx documentation for your product.  E.g.::

 extensions = ['sphinx.ext.autodoc',
               'sphinx.ext.doctest',
               'qubic.sphinx.graphvizinclude',
              ]


Using the Extension
-------------------

At appropriate points in your document, call out the interface
autodocs via::

  .. graphvizinclude:: ./path_to/graph_definition.dot

