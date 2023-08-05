# -*- encoding: UTF-8 -*-
'''
Created on 30 mars 2010

@author: thierry
'''
import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages
setup(name='zourite',
      version='0.4.0',
      package_dir = {'': 'src'},
      packages= find_packages(),
      scripts=['scripts/zourite','scripts/zourite-setup','scripts/zourite-setup-force'],
      package_data={'zourite': ['*.png']},    
      data_files=[('/usr/share/applications/hildon',['hildon/zourite.desktop']),
                  ('/usr/share/icons/hicolor/48x48/hildon',['hildon/icons/48x48/zourite.png']),
                  ('/usr/share/icons/hicolor/64x64/hildon',['hildon/icons/64x64/zourite.png'])],  
      author='Thierry Bressure',
      author_email='thierry@bressure.net',
      maintainer='Thierry Bressure',
      maintainer_email='zourite@bressure.net',
      url='http://blog.zourite.bressure.net',
      download_url='http://zourite.bressure.net',
      description='Zourite Professional Networking Application for N900',
      long_description='Zourite is a client for professional Network like LinkedIn. You can stay connected to your contacts and manage you network.',
      classifiers=[
          'Development Status :: 4 - Beta',
          "Environment :: Handhelds/PDA's",          
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',          
          'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python',
          'Topic :: Communications :: Email',
          'Topic :: Office/Business',          
          ],
      zip_safe=False

      )


