splunk-elasticsearch
====================

I have created a small search command for Splunk which will allow you to search Elastic Search and display the results in the Splunk GUI


I have only Proof of concepted this in my splunk enviroment, but should be revising it shortly to be better.

Steps to use

Install ElasticSearch Python module "pip install elasticsearch " i think (I'll update with more details)

In my POC copy the files in:

the bin directory to $SPLUNK_HOME/etc/apps/search/bin
the local directory to $SPLUNK_HOME/etc/apps/search/local 

and reload your splunk

Now you should be able to do a simple search like 

| es | search Event="*SOMETHING*" 

