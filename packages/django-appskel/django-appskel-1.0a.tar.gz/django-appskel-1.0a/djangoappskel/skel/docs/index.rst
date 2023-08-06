.. {{ egg }} documentation master file, created by
   sphinx-quickstart on Tue Sep 15 10:47:03 2009.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

######################################
Welcome to {{ egg }}'s documentation!
######################################

This document refers to version |release|

***************
Getting Started
***************

.. toctree::
    :maxdepth: 2
    :numbered:

{% if repo %}
**************************************
Contributing to {{ egg }}
**************************************

.. toctree::
    :maxdepth: 2
    :numbered:

    contribution

{% endif %}

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
