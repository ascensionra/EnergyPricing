# EnergyPricing
Collection of datasets for aggregating into a comprehensive energy price resource

Module/eia.py
*******************************
Written for Python 2.7
Requires:
  requests
  json
  sys
  re
*******************************
How to use the module:
*******************************
This module requires an API key for the EIA.gov datastore: http://www.eia.gov/beta/api/index.cfm

This module is written against the Oracle REST API provided by University of Texas professor Dr. Cannata, but can be modified to work with any RESTful interface. Some of the SQL statements may need to be tweaked, but they are pretty agnostic in regards to SQL platform. Primarily the createTable statements are suspect. Query quoting when building the URLs is particularly important.

This module uses the python module 'requests', so you will need to craft your headers for the particular REST interface you are coding against. See eia.py for the header structure required for the Oracle REST API this was originally intended for.

Some of the key uses of this 'module' are to create/empty/delete tables and insert records for a given SQL database, with enough abstraction that you only have to worry about providing the data (formatted as JSON.)

Basically, the key usefullness is in obtaining a list of interesting series (see Module/series.py to do this in bulk,) create the table(s), and insert the records. Then, process with your favorite data analysis tool (SQL Developer, KNIME, etc.)

*******************************
PullJson.py *DEPRECATED*
*******************************

