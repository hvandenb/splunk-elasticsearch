#!/usr/bin/python
from datetime import datetime
from elasticsearch import Elasticsearch
import pprint
import time
import sys
import io
import csv

total = len(sys.argv)
cmdargs = str(sys.argv)
index="*";
limit=100;
oldestDate="now";
earlietDate="now-1d";
defaultField="message";
for i in xrange(total):
   opt = str (sys.argv[i]);
   if (  opt.startswith("index") ):
      index= str (sys.argv[i]).split("=")[1];
   elif (  opt.startswith("query") ):
      query= str (sys.argv[i]).split("=")[1];
   elif (  opt.startswith("field") ):
      startDate= str (sys.argv[i]).split("=")[1];
   elif (  opt.startswith("oldest") ):
      oldestDate= str (sys.argv[i]).split("=")[1];
   elif (  opt.startswith("earl") ):
      earliest= str (sys.argv[i]).split("=")[1];
   elif (  opt.startswith("limit") ):
      limit= str (sys.argv[i]).split("=")[1];
   
pp = pprint.PrettyPrinter(indent=4)
es = Elasticsearch()
res = es.search(size=50, index=index, body={
      "size": limit,
      "query": {
         "filtered" : {
            "query": {
               "match_all": {}
            },
            "filter" : {
                "range" : {
                    "@timestamp": {
                        "gt" : earlietDate,
                        "lt" : oldestDate
                    }
                }
            }
        }
       } 
   })
print("\"_time\",\"_raw\",\"index\",\"type\"")
#pp.pprint(res);
date_time = '2014-12-21T16:11:18.419Z'
pattern = '%Y-%m-%dT%H:%M:%S.%fZ'
output = io.StringIO()
writer = csv.DictWriter(output)
writer.writeheader()
for stats in my_stats:
    writer.writerow(res['hits']['hits'])
csv_output = output.getvalue().encode('utf-8')
print "%s" % csv_output
#test development branch