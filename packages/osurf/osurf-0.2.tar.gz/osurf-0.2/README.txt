Surf / SPARQL back-end for ORDF

Installing requires surf.sparql_protocol which does not install
with pip. So first do:

	easy_install -U surf.sparql_protocol

and then install this package as usual.

In your config, put:

	ordf.readers = surf
	ordf.writers = surf
	surf.endpoint = http://localhost:8890/sparql

Minimally, virtuoso needs this command run in isql:

	grant SPARQL_UPDATE to "SPARQL";

note that this gives anyone with access to the sparql endpoint
write access to the store. For production use, make a different
sparql endpoint with write access and make sure it is only
accessible from trusted application hosts, and let the world
at the public endpoint.
