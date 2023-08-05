#!/usr/bin/env python
from distutils.core import setup

setup(name='Pweave',
      version='0.12',
      description='Literate programming with reST or LaTeX in Sweave style',
      author='Matti Pastell',
      author_email='matti.pastell@helsinki.fi',
      url='http://mpastell.com/pweave',
      packages=['Pweave'],
      license=['GPL'],
      scripts=['Pweave/Pweave'],
      classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Text Processing :: Markup',
        'License :: OSI Approved :: GNU General Public License (GPL)'],
      long_description = """Pweave is a literate programming tool for Python that is developed after Sweave. Like Sweave it uses the noweb syntax. Pweave is a single python script that is able to weave a python code between <<>>= and @ blocks and include the results in the document. Additionally it can capture matplotlib figures. It supports reST, Sphinx and Latex markup. Pweave is good for creating dynamic reports and tutorials. It can also be used to make websites together with Sphinx or rest2web."""
      
)
