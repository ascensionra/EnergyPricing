# EnergyPricing
Collection of datasets for aggregating into a comprehensive energy price resource

PullJson.py
*******************************
Written for Python 2.7
Required python modules:
json
os
urllib
urllib2
us
*******************************
How to use the script:
*******************************
As of now, the script will run and generate output to a relative direcotry of ./output/tmp. A list of series id
values need to be supplied to the 'constructor', along with an API token (currently hardcoded in the script.)

There is a function to generate filenames/series id values for datasets that are available at the state level, 
but it needs to be generalized, as it is being used for the ELEC.REV.XX-ALL.M series specifically.

Use the examples to add more lists of data sources.

TODO: Expand the script to accept a filename containing series to import.
*******************************
*******************************

Planned development
*******************************
Scripting to expand SQL automation by connecting to database and performing record INSERTION.
Maintain a separate table to store 'updated' fields from datasets to prevent duplicating records. Using this in
conjunction with PullJson.py to adjust API call to only retirieve missing data would be ideal.

