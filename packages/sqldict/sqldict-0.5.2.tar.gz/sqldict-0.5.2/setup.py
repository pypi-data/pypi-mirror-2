
from distutils.core import setup
from sqldict import sqldict

setup(name='sqldict',
      description='sqldict - You have a dict of unlimited capacity providing transparent object serialization, its up to you now.',
      author='Krister Hedfors', 
      author_email='krister.hedfors+sqldict@gmail.com', 
      version='0.5.2',
      packages=['sqldict'], 
      #data_files=[('sqldict','__init__.py'),  ('sqldict', 'sqldict.py')], 
      long_description=sqldict.__doc__
)

