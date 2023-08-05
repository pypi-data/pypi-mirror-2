import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = ['repoze.bfg==1.2', 'repoze.catalog', 'Pygments']

setup(name='pysourcesearch',
      version='0.1',
      description='a repoze.bfg wsgi app to provide a search engine for your python packages',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: BFG",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Nathan Van Gheem',
      author_email='vangheem@gmail.com',
      url='',
      keywords='web wsgi bfg catalog python source search',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="sourcesearch",
      entry_points = """\
      [paste.app_factory]
      app = pysourcesearch.run:app
      """
      )

