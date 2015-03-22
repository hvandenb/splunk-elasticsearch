#!/usr/bin/env python
#
# Copyright 2011-2014 Splunk, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


# python essearch.py __EXECUTE__ 'location="New York"'

from datetime import datetime
from elasticsearch import Elasticsearch
import pprint
import time
import sys
 
from splunklib.searchcommands import \
  dispatch, GeneratingCommand, Configuration, Option, validators

@Configuration()
class ElasticCommand(GeneratingCommand):

  index = Option(require=False, default=*)

  q = Option(require=False)

  fields = Option(require=False, default="message")

  oldest = Option(require=False, default="now")

  earl = Option(require=False, default="now-1d")

  limit = Option(require=False, validate=validators.Integer(), default=100)

  def generate(self):
    config = self.get_configuration()
 
    pp = pprint.PrettyPrinter(indent=4)
    es = Elasticsearch()
    body = {
          "size": limit,
          "query": {
             "filtered" : {
                "query": {
                      "query_string" : {
                            "default_field" : defaultField,
                            "query" : query
                      }
                },
                "filter" : {
                       "range" : {
                           "@timestamp": {
                               "lt" : earliestDate,
                               "gt" : oldestDate
                           }
                       }
                }
            }
           } 
       }
    #pp.pprint(body);
    res = es.search(size=50, index=index, body=body);

    # if response.status_code != 200:
    #   yield {'ERROR': results['error']['text']}
    #   return


    # date_time = '2014-12-21T16:11:18.419Z'
    # pattern = '%Y-%m-%dT%H:%M:%S.%fZ'

    for hit in res['hits']['hits']:
      yield self.getEvent(hit)

  def getEvent(self, result):

    # hit["_source"][defaultField] = hit["_source"][defaultField].replace('"',' ');
    # epochTimestamp = hit['_source']['@timestamp'];
    # hit['_source']['_epoch'] = int(time.mktime(time.strptime(epochTimestamp, pattern)))
    # hit['_source']["_raw"]=hit['_source'][defaultField]

    event = {'_time': time.time(), 
             '_index': result['_index'], 
             '_type': result['_type'], 
             '_id': result['_id'],
             '_score': result['_score']
            }

    event["_raw"] = json.dumps(result)

    return event

  def get_configuration(self):
    sourcePath = os.path.dirname(os.path.abspath(__file__))
    config_file = open(sourcePath + '/config.json')
    return json.load(config_file)

dispatch(ElasticCommand, sys.argv, sys.stdin, sys.stdout, __name__)