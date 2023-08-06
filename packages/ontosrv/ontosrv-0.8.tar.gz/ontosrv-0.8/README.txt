The ORDF Ontology Server -- a simple Pylons Application
=======================================================


Installation and Setup
======================

Install ORDF and OntoSrv using pip::

    pip install rdflib==2.4.2
    pip install -e hg+http://ordf.org/src/#egg=ordf
    pip install -e hg+http://ordf.org/src/ontosrv/#egg=ontosrv

Make a config file as follows::

    paster make-config ontosrv development.ini

Tweak the config file as appropriate and then setup the application::

    paster setup-app development.ini

Make the data directory (depending on what you have put in the config
file, the default is "data" in the current directory)::

    mkdir data

Install some fixtures and initial data::

    ordf_load_n3
    ordf_load_n3 -p ordf.onto -b http://ordf.org/lens/

Install some optional packages::

    pip install docutils

Run a testing webserver::

    paster serve development.ini

Point a web browser at http://localhost:5000/graph?uri=http://ordf.org/schema/ordf
and enjoy!
