# -*- encoding: utf-8 -*-

"""
The Initialization File for the Skeleton Repository

The skeleton repository will serve as the backbone of configuration
for neuralNOD INC. and the folder is configured with `__init__.py`,
and though there is no module not yet defined for `skeleton` it is
the responisibility of the end user to create a virtual environment
and thus may not confuse with the use of `skeleton` files/submodule.

The init-time option registrations is for selected functions, the
major functions are fetched directly by module import.

@author:  nxlogics
"""

from .connections import DBConnection # noqa: F401, F403
