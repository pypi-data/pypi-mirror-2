#!/usr/bin/env python
#Copyright (c) 2008 Erik Tollerud (etolleru@uci.edu) 
from __future__ import division,with_statement

from glob import glob
from distribute_setup import use_setuptools
use_setuptools()
from setuptools import setup,find_packages
from distutils.command.build_py import build_py as du_build_py

from astropysics.version import version as versionstr

#custom build_py overwrites version.py with a version overwriting the revno-generating version.py
class apy_build_py(du_build_py):
    def run(self):
        from os import path
        res = du_build_py.run(self)
        
        versfile = path.join(self.build_lib,'astropysics','version.py')
        print 'freezing version number to',versfile
        with open(versfile,'w') as f: #this overwrites the actual version.py
            f.write(self.get_version_py())
        
        return res
        
    def get_version_py(self):
        import datetime
        from astropysics.version import _frozen_version_py_template
        from astropysics.version import version,major,minor,bugfix,dev
        
        
        timestamp = str(datetime.datetime.now())
        t = (timestamp,version,major,minor,bugfix,dev)
        return _frozen_version_py_template%t
        
#custom sphinx builder just makes the directory to build if it hasn't already been made
try:
    from sphinx.setup_command import BuildDoc
    
    class apy_build_sphinx(BuildDoc):
        def finalize_options(self):
            from os.path import isfile    
            from distutils.cmd import DistutilsOptionError
            
            if self.build_dir is not None:
                if isfile(self.build_dir):
                    raise DistutilsOptionError('Attempted to build_sphinx into a file '+self.build_dir)
                self.mkpath(self.build_dir)
            return BuildDoc.finalize_options(self)
            
except ImportError: #sphinx not present
    apy_build_sphinx = None
    
descrip = """
`astropysics` contains a variety of utilities and algorithms for reducing, analyzing, and visualizing astronomical data.
      
See http://packages.python.org/Astropysics/ for detailed documentation.
"""

cmdclassd = {'build_py' : apy_build_py}
if apy_build_sphinx is not None:
    cmdclassd['build_sphinx'] = apy_build_sphinx
 

apyspkgs = find_packages()
#extra/recommended packages
_extras = ['matplotlib','pyfits','ipython','networkx','pygraphviz']
_guiextras = ['traits','traitsGUI','chaco']
_gui3dextras = ['mayavi']

scripts = glob('scripts/*')

setup(name='Astropysics',
      version=versionstr,
      description='Astrophysics libraries for Python',
      
      packages=apyspkgs,
      package_data={'astropysics':['data/*']},
      scripts=scripts,
      requires=['numpy','scipy'],
      install_requires=['numpy','scipy'],
      provides=['astropysics'],
      extras_require={'all':_extras+_guiextras+_gui3dextras,
                      'allnogui':_extras,
                      'allno3d':_extras+_guiextras},
      
      author='Erik Tollerud',
      author_email='etolleru@uci.edu',
      license = 'Apache License 2.0',
      url='http://www.physics.uci.edu/~etolleru/software.html#astropysics',
      long_description=descrip,
      cmdclass = cmdclassd
     )
