from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='islay.auth',
      version=version,
      description="An unobtrusive authentication framework for WSGI stacks.",
      long_description=open(os.path.join('src', 'islay', 'auth', 'README.txt')).read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: BSD License",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware",
        "Topic :: Security",
        ],
      keywords='wsgi python authentication repoze.who',
      author='Matthew Wilkes',
      author_email='wilkes@jarn.com',
      url='http://code.google.com/p/islay/',
      license='Modified BSD',
      package_dir = {'':'src'},
      packages=find_packages('src', exclude=['ez_setup']),
      namespace_packages=['islay'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'distribute',
          'WebOb',
          'zope.interface',
      ],
      entry_points="""
            [paste.filter_factory]
            auth = islay.auth.auth:AuthFactory
      """,
      )
