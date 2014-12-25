#!/usr/bin/python
from datetime import datetime
from elasticsearch import Elasticsearch
import pprint
import time
import sys
 
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

for hit in res['hits']['hits']:
   hit["_source"][defaultField] = hit["_source"][defaultField].replace('"',' ');
   epochTimestamp = hit['_source']['@timestamp'];
   hit['_source']['_epoch'] = int(time.mktime(time.strptime(epochTimestamp, pattern)))
   hit['_source']["_raw"]=hit['_source'][defaultField]
   print("%(_epoch)s,\"%(_raw)s\"," % hit["_source"] + 
         "\"%(_index)s\",\"%(_type)s\"" % hit
         )
#test development branch