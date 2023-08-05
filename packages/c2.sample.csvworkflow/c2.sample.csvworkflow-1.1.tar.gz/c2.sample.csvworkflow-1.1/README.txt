Introduction
============

The collective.wtf is a product that applies csv formatted workflow to plone workflow.
The c2.sample.csvworkflow is a sample workflow application that uses collective.wtf a base product.
This application have utility functions to ease plone workflow scheme setting.


Dependence
==========

To load csv formatted workflow, collective.wtf is required.
This product will also install it automatically.


Install
=======

To install c2.sample.csvworkflow on your system, add c2.sample.csvworkflow in eggs of buildout.cfg.

::

    eggs = 
        c2.sample.csvworkflow


Testing
=======

Execution command is following.

::

    $ ./bin/instance test -s c2.sample.csvworkflow     # Case of Plone3.x

::

    $ ./bin/test -s c2.sample.csvworkflow     # Case of Plone4.x
