# -*- coding: utf-8 -*-
"""
    flaskext.fluiddb
    ~~~~~~~~~~~~~~~~

    Flask integration for FluidDB

    :copyright: (c) 2010 by Ali Afshar <aafshar@gmail.com>.
    :license: MIT, see LICENSE for more details.
"""

from fom.dev import sandbox_fluid
from fom.session import Fluid


__all__ = ['init_fluiddb']


def init_fluiddb(app, sandbox=False):
    """Start and bind the FluidDB client

    :param app: The Flask instance
    :param sandbox: Whether to use the sandbox, optional, default: False
    """
    if sandbox:
        fluid = sandbox_fluid()
    else:
        fluid = Fluid()
        fluid.bind()
    app.fluiddb = fluid
    return fluid


