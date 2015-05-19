# EnergyPricing
Collection of python tools for aggregating EIA API data into a comprehensive energy price resource 

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

This module will require a LAST_UPDATE table in your database (VARCHAR,VARCHAR,DATE) to keep track of the most recent data update per table. With the potential to access millions of records in the EIA datastore, you can quickly come up against the API call limit, and you can lose your license.

Some of the key uses of this 'module' are to create/empty/delete tables and insert records for a given SQL database, with enough abstraction that you only have to worry about providing the data (formatted as JSON.)

Basically, the key usefullness is in obtaining a list of interesting series (see Module/series.py to do this in bulk,) create the table(s), and insert the records. Then, process with your favorite data analysis tool (SQL Developer, KNIME, etc.)

*******************************
Notes about the EIA API
*******************************
This API is in beta, so it is evolving. I've tried to abstract this module enough so that changes made to the API don't impact the usefullness of this project. They have added some interesting features, like the Updates query http://1.usa.gov/1INyOev, but there's no direct way (in the documentation, at least) to specify a date range. A LAST_UPDATE table, as described above, is key to accessing only the information that is missing from your own dataset. This feature is key for future development of an automated process to keep the tables current. 

*******************************
PullJson.py *DEPRECATED*
*******************************

