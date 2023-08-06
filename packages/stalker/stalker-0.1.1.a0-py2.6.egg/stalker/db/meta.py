#-*- coding: utf-8 -*-
"""This module exists to have a singleton metadata. The best way is to hold the
metadata variable in a seperate module (as Guido van Rossum suggested, if I
remember correctly)

"""

from sqlalchemy import MetaData
#from beaker import session as beakerSession


# SQLAlchemy database engine
engine = None

# SQLAlchemy session manager
session = None

# the singleton metadata
metadata = MetaData()

# a couple off helper attributes
__mappers__ = []
