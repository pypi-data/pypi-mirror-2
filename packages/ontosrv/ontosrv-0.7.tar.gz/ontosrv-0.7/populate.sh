#!/bin/sh

### shell script to pull schema definitions from ordf.org

ordf -c development.ini -x -s -m "populate data from ordf.org..." \
	http://ordf.org/schema/ordf \
	http://ordf.org/lens/changeset \
	http://ordf.org/lens/fresnel \
	http://ordf.org/lens/ontology \
	http://ordf.org/lens/rdfs
