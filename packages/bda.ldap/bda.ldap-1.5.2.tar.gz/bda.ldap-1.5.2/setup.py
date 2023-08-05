from setuptools import setup, find_packages
import sys, os

version = '1.5.2'
shortdesc = "LDAP convenience library"
longdesc = open(os.path.join(os.path.dirname(__file__), 'README.txt')).read()

setup(name='bda.ldap',
      version=version,
      description=shortdesc,
      long_description=longdesc,
      classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Web Environment',
            'Framework :: Zope2',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content',            
      ], # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Robert Niederreiter',
      author_email='dev@bluedynamics.com',
      url='https://svn.plone.org/svn/collective/bda.ldap',
      license='General Public Licence',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['bda'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'python-ldap',
          'zodict',
          'bda.cache',
      ],
      extras_require={
          'test': [
              'interlude',
              'zope.configuration',
              'zope.testing',        
          ]
      },
      entry_points="""
      """,
      )
