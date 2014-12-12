from datetime import datetime
from elasticsearch import Elasticsearch
import pprint
pp = pprint.PrettyPrinter(indent=4)
es = Elasticsearch()

res = es.search(size=50, index="nagios-*", body={"query": {"match_all": {}}})
print("\"_time\",\"Event\"")
for hit in res['hits']['hits']:
   hit["_source"]["message"] = hit["_source"]["message"].replace('"',' ');
   print("%(@timestamp)s,\"%(message)s\" " % hit["_source"])
   #pp.pprint(hit);
