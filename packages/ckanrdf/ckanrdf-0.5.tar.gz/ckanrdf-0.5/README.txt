Tools for generating RDF from CKAN instances
============================================

See the Installation section below for installation instructions

Usage is driven by a configuration file that can be created with
the command

	$ paster make-config ckanrdf myconfig.ini

You can then edit myconfig.ini to suit your needs. Once configured
RDF can be generated from a CKAN instance using any serialisation
supported by RDFLib for any package in the remote catalogue.

For example,

	$ paster ckanrdf -o - -d myconfig.ini wordnet

with an unmodified, default configuration should generate the triples
for the wordnet package in N3 format.

Installation
============

We use pip for installation and recommend the use of virtualenv.
Make sure pip and virtualenv are installed using your standard
system installation tools or easy install

First download the source package, possibly from the mercurial
repository:

	$ hg clone http://bitbucket.org/ww/ckanrdf/

(optional) Create a virtualenv and activate it:

	$ virtualenv /some/where/ckanrdf
	$ . /some/where/ckanrdf/bin/activate

Install the dependencies with pip

	$ pip install -r pip-requirements.txt

Alternatively you can install with setuptools using

	$ python setup.py install

However mind that if you are using setuptools you have to make
sure to have RDFLib installed before ckanrdf will work as it is 
not mentioned in setuptools dependency list due to some issues
with the development branch. Version 2.4.2 of RDFLib is fine.
