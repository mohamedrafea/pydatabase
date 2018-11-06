from distutils.core import setup

setup(name='pydatabase',
      version='1.0.0',
      description='Database layer on top of SQLAlchemy',
      author='Mohamed Rafea',
      author_email='mohamed.rafea@gmail.com',
      url='https://github.com/mohamedrafea/pydatabase',
      packages=['pydatabase','pydatabase.env','pydatabase.table','pydatabase.dimension','tests','tests.table']
     )