from setuptools import setup, find_packages
import sys, os

version = '1.0'
shortdesc = "Pack (multiple) databases (ZODB) on Zope ZEO servers"
longdesc = open(os.path.join(os.path.dirname(__file__), 'README.txt')).read()
longdesc += open(os.path.join(os.path.dirname(__file__), 'LICENSE.txt')).read()

setup(name='bda.zeopack',
      version=version,
      description=shortdesc,
      long_description=longdesc,
      classifiers=[
            'Framework :: ZODB',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'License :: OSI Approved :: BSD License',
      ], 
      keywords='',
      author='Jens W. Klein',
      author_email='jens@bluedynamics.com',
      url='http://pypi.python.org/pypi/bda.zeopack',
      license='BSD License',
      packages = find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['bda'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',                
          'ZODB3',        
          # -*- Extra requirements: -*
      ],
      entry_points={
        'console_scripts':[
            'zeomultipack = bda.zeopack.main:main',
            ]
        },     
)

