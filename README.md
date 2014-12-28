splunk-elasticsearch
====================

I have created a small search command for Splunk which will allow you to search Elastic Search and display the results in the Splunk GUI


This project is now a valid splunk application and installs as you would any other splunk applications

Steps to use
Install python if it is not installed

Install ElasticSearch https://github.com/elasticsearch/elasticsearch-py
"pip install elasticsearch "

<<<<<<< HEAD
In my POC copy the files in:

the bin directory to $SPLUNK_HOME/etc/apps/search/bin
the local directory to $SPLUNK_HOME/etc/apps/search/local 

===============================================
=======
git clone "This Project"
rsync -av splunk-elasticsearch $SPLUNK_HOME/etc/apps
>>>>>>> 7a1c3de14cfcdf8faf679216cb3bd7bce856ed60

Now you should be able to do a simple search like 
| esearch | top message

or 
| esearch oldest=now-100d earliest=now query="some text" index=nagios* limit=1000 field=message

================================================

command reference:
esearch
    oldest = default (now-1d)   uses elasticsearch timedate value or function
    earliest = default (now)    uses elasticsearch timedate value or function
    index    = default (*)      sepecify the elasticsearch index to search
    limit    = default (50)     number of records to return
    field    = default ("message")  which elasticsearch field to query and return the value
    query    = default ("*" | might change this to match_all)   the elasticsearch query_string
    


<<<<<<< HEAD
=======
| esearch oldest=now-40d earliest=now limit=1000 index=nagios* | search *SOMETHING*" 
>>>>>>> 7a1c3de14cfcdf8faf679216cb3bd7bce856ed60

