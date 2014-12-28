splunk-elasticsearch
====================

I have created a small search command for Splunk which will allow you to search Elastic Search and display the results in the Splunk GUI


I have only Proof of concepted this in my splunk enviroment, but should be revising it shortly to be better.

Steps to use

Install ElasticSearch https://github.com/elasticsearch/elasticsearch-py
"pip install elasticsearch "

In my POC copy the files in:

the bin directory to $SPLUNK_HOME/etc/apps/search/bin
the local directory to $SPLUNK_HOME/etc/apps/search/local 

===============================================

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
    



