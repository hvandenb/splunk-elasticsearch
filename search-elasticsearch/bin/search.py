#!/usr/bin/python
from datetime import datetime
from elasticsearch import Elasticsearch
import pprint
import time
import sys
 
total = len(sys.argv)
cmdargs = str(sys.argv)
index="*";
for i in xrange(total):
   opt = str (sys.argv[i]);
   if (  opt.startswith("index") ):
      index= str (sys.argv[i]).split("=")[1];
   elif (  opt.startswith("query") ):
      query= str (sys.argv[i]).split("=")[1];
   
pp = pprint.PrettyPrinter(indent=4)
es = Elasticsearch()
res = es.search(size=50, index=index, body={
      "query": {
         "filtered" : {
            "query": {
               "match_all": {}
            },
            "filter" : {
                "range" : {
                    "@timestamp": {
                        "gt" : "now-1w",
                        "lt" : "now"
                    }
                }
            }
        }
       } 
   })
print("\"_time\",\"_raw\",\"index\",\"type\"")
pp.pprint(res);
for hit in res['hits']['hits']:
   hit["_source"]["message"] = hit["_source"]["message"].replace('"',' ');
   epochTimestamp = hit['_source']['@timestamp'];
   date_time = '2014-12-21T16:11:18.419Z'
   pattern = '%Y-%m-%dT%H:%M:%S.%fZ'
   hit['_source']['_epoch'] = int(time.mktime(time.strptime(epochTimestamp, pattern)))
   print("%(_epoch)s,\"%(message)s\"," % hit["_source"] + 
         "\"%(_index)s\",\"%(_type)s\"" % hit
         )