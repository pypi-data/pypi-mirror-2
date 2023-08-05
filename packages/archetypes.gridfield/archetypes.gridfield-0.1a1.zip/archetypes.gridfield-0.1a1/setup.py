from setuptools import setup, find_packages
import os

version = '0.1a1'

tests_require = ['collective.testcaselayer']

setup(name='archetypes.gridfield',
      version=version,
      description="Datagrid for Archetypes content, rows based on z3c.form",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='datagrid archetypes plone jquery overlay',
      author='Matous Hora, Radim Novotny - DMS4U',
      author_email='info@dms4u.cz',
      url='http://pypi.python.org/pypi/archetypes.gridfield',
      license='GPL',
      packages=find_packages('src', exclude=['ez_setup']),
      package_dir = {'':'src'},
      namespace_packages=['archetypes'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.z3cform>=0.5.10',
          'plone.app.z3cform',
          'plone.app.jquerytools',
      ],
      tests_require=tests_require,
      extras_require={'tests': tests_require,
                      'example': ['archetypes.schemaextender']},
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
