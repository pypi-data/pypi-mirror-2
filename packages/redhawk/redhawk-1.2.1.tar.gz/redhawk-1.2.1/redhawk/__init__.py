import os

__version__ = '1.2.1'
DB_NAME = '.redhawk_db'

def GetVersion():
  return __version__

def GetDBName():
  return DB_NAME
