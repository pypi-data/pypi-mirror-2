#!/usr/bin/env python
from setuptools import setup, find_packages

setup (
     name = "topzootools",
     version = "0.0.3",
     description = 'Processing and conversion tools for Internet Topology Zoo',

     long_description='Processing and conversion tools for Internet Topology Zoo',
               
     # simple to run 
     entry_points = {
         'console_scripts': [
             'zoomerge = TopZooTools.merge.py:main',    
             'zooconvert = TopZooTools.convert.py:main',
         ],
     },


     author='Simon Knight',
     author_email="simon.knight@adelaide.edu.au",
     url="http://packages.python.org/topologyzootools/",
     packages=['TopZooTools'],  
     
     package_data = {'': []},
                                                                                                   
     download_url = "http://bandicoot.maths.adelaide.edu.au/topology_zoo",
     install_requires=['mako', 'networkx', 'matplotlib', 'numpy',],
     classifiers = [
         "Programming Language :: Python",
         "Development Status :: 3 - Alpha",
         "Intended Audience :: Science/Research",
         "Intended Audience :: System Administrators",
         "Intended Audience :: Telecommunications Industry",
         "License :: Other/Proprietary License",
         "Operating System :: MacOS :: MacOS X",
         "Operating System :: POSIX :: Linux",
         "Topic :: System :: Networking",
         "Topic :: System :: Software Distribution",
         "Topic :: Scientific/Engineering :: Mathematics",
         ],     
 
)
