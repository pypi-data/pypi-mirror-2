
from distutils.core import setup

setup(name='sqldict',
      description='sqldict - dict with sqlalchemy database-agnostic back-end',
      author='Krister Hedfors', 
      author_email='krister.hedfors+sqldict@gmail.com', 
      version='0.4.1',
      packages=['sqldict'], 
      #data_files=[('sqldict','__init__.py'),  ('sqldict', 'sqldict.py')], 
      long_description='''
      sqldict - dict with sqlalchemy database-agnostic back-end
'''
)

