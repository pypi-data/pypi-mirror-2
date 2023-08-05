"""
"""

from distutils.core import setup

version = '0.2'

long_description='''
Playdoh is an easy-to-use open-source Python library for distributing
computations over multiple cores and machines. It provides an
interface to distribute a Python function or optimize any fitness function 
over multiple CPUs, GPUs or machines connected over a network. 
'''

if __name__=="__main__":
    setup(name='playdoh',
      version=version,
      py_modules=[],
      packages=['playdoh',
                'playdoh.optalg'],
      requires=['numpy(>=1.3.0)',
                'multiprocessing'],
      url='http://code.google.com/p/playdoh/',
      description='Open-source library for distributing computations over multiple cores and machines',
      long_description=long_description,
      author='Cyrille Rossant, Dan Goodman',
      author_email='Cyrille.Rossant at ens.fr',
      download_url='http://code.google.com/p/playdoh/downloads/list',
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering'
        ]
      )