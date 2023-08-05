.. Flask FluidDB documentation master file, created by
   sphinx-quickstart on Wed Jul 28 20:47:33 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Flask FluidDB
=============

This extension allows easy access to Fluiddb from Flask. A Fluiddb session is
bound, returned, and for convenience tagged to the application isntance.

Using::

    from flask import Flask
    from flaskext.fluiddb import init_fluiddb

    app = Flask(__name__)
    fluid = init_fluiddb(app)

    # start using Fluiddb
    fluid.tags[u'fluiddb/about'].get(returnDescription=True)

    # or alternatively, for convenience
    app.fluid.tags[u'fluiddb/about'].get(returnDescription=True)


API:

    .. autofunction:: flaskext.fluiddb.init_fluiddb


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

