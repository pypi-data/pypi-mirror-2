from setuptools import setup, find_packages

version = '0.2'

setup(name='vimpdbhook',
      version=version,
      description="A PDB hook for MacVIM",
      long_description=file("README").read(),
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Stefan ELetzhofer',
      author_email='stefan.eletzhofer@inquant.de',
      license='BSD',
      url="https://vimpdbhook.googlecode.com/svn/trunk",
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          "setuptools",
          "appscript"
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
