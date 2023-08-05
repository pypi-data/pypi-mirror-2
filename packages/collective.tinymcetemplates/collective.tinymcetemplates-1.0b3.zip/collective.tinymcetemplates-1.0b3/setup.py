from setuptools import setup, find_packages
import os

version = '1.0b3'

setup(name='collective.tinymcetemplates',
      version=version,
      description="TinyMCE Plugin for templates and snippets",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='TinyMCE Plone template snippet',
      author='Rob Gietema',
      author_email='rob@fourdigits.nl',
      url='http://pypi.python.org/pypi/collective.tinymcetemplates',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.app.registry',
          'Products.TinyMCE',
      ],
      extras_require={
        'test': ['collective.testcaselayer', ],
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
