from setuptools import setup, find_packages
import os

version = '0.1alpha'

setup(name='uniba.bandilavoro',
      version=version,
      description="Add-on per la gestione delle pubblicazione di bandi cococo/pro/autonomo per le esigenze dei Dipartimenti di ricerca e non",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='universita, istruzione, bandi',
      author='Vito Falco - Universita\' degli studi di Bari Aldo Moro',
      author_email='vito.falco@uniba.it',
      url='http://www.uniba.it',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['uniba'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'collective.js.datatables',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )
