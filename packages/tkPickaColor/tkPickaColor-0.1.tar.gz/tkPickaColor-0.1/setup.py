#from distutils.core import setup
from setuptools import setup

setup(name='tkPickaColor',
      version='0.1',
      description='Tkinter dialog to provide Linux developers a more full featured color chooser',
      author='Steve Solomon',
      author_email='codeduffer@gmail.com',
      classifiers = [
      'Development Status :: 3 - Alpha',
       'Intended Audience :: Developers',
       'License :: OSI Approved :: GNU General Public License (GPL)', 
       'Natural Language :: English', 
       'Operating System :: POSIX :: Linux',
       'Programming Language :: Python :: 2.6',
       'Topic :: Software Development :: Widget Sets'],
      packages = ['tkPickaColor'], 
      package_dir={'tkPickaColor': 'tkPickaColor'}, 
      package_data= {'tkPickaColor': ['resources/spectrum.gif', 'resources/grayvalues.gif', "cheatsheet.txt"]})
