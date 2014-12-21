#!/usr/bin/python
from datetime import datetime
from elasticsearch import Elasticsearch
import pprint
import time

pp = pprint.PrettyPrinter(indent=4)
es = Elasticsearch()

res = es.search(size=50, index="*", body={"query": {"match_all": {}}})
print("\"_time\",\"_raw\"")
for hit in res['hits']['hits']:
   hit["_source"]["message"] = hit["_source"]["message"].replace('"',' ');
   epochTimestamp = hit['_source']['@timestamp'];
   date_time = '2014-12-21T16:11:18.419Z'
   pattern = '%Y-%m-%dT%H:%M:%S.%fZ'
   hit['_source']['_epoch'] = int(time.mktime(time.strptime(epochTimestamp, pattern)))
   print("%(_epoch)s,\"%(message)s\" " % hit["_source"] )