OVERVIEW:
=========

The python Fusion Tables Client library helps you connect and run queries on 
your tables in Fusion Tables.

You can select 2 methods of authentication: OAuth or Client Login.
The python-oauth2 library is used for OAuth.

Two helper classes have been included in this library to make coding
easier: CSVImporter and SQL. 

CSVImporter allows you to create a new table from an existing CSV file.

SQL builds SQL statements for you, in case you don't want to fully type out
"SELECT ..." or "INSERT ..." every time. 

Note
****

This is a fork of the original python fusion tables client available at http://code.google.com/p/fusion-tables-client-python/, forked it to package it for use with pip & pypi.

DEPENDENCIES:
=============

- python-oauth2 library: http://github.com/simplegeo/python-oauth2
- python-oauth2 dependency, httplib2: http://code.google.com/p/httplib2/

