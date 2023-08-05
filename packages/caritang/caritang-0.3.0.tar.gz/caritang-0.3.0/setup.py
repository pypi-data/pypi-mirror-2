# -*- encoding: UTF-8 -*-
'''
Created on 5 avr. 2010

@author: thierry
'''
from distutils.core import setup
setup(name='caritang',
      version='0.3.0',
      package_dir = {'': 'src'},
      packages=['caritang',
                'caritang.common',
                'caritang.core',
                'caritang.gui'],               
      scripts=['scripts/caritang'],
      package_data={'caritang': ['*.png']},      
      author='Thierry Bressure',
      author_email='thierry@bressure.net',
      maintainer='Thierry Bressure',
      maintainer_email='caritang@bressure.net',
      url='http://blog.caritang.bressure.net',
      download_url='http://caritang.bressure.net',
      description='Caritang a simple backup application for N900 to google docs',
      long_description='Caritang let you to upload content of your N900 into a google docs account. You can specify which data to backup',
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          "Environment :: Handhelds/PDA's",          
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',          
          'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python',
          'Topic :: System :: Archiving :: Backup'
          ],

      )


