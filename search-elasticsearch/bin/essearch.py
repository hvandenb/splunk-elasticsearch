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


# python essearch.py __EXECUTE__ 'q="New York"'

from datetime import datetime
from elasticsearch import Elasticsearch
import os, sys, time, requests, oauth2, json, urllib
#import splunk.Intersplunk

#(isgetinfo, sys.argv) = splunk.Intersplunk.isGetInfo(sys.argv)

from splunklib.searchcommands import \
  dispatch, GeneratingCommand, Configuration, Option, validators

@Configuration()
class EsCommand(GeneratingCommand):
  """ Generates events that are the result of a query against Elasticsearch

  ##Syntax

  .. code-block::
      es index=<string> | q=<string> | fields=<string> | oldest=<string> | earl=<string> | limit=<int> body="{
    \"size\": 10,
    \"query\": {
           \"filtered\": {
               \"query\": {
                   \"query_string\": {
                       \"query\": \"*\"
                   }
               }
           }
       }
    }"


  ##Description

  The :code:`es` issue a query to ElasticSearch, where the
  query is specified in :code:`q`.

  ##Example

  .. code-block::
      | es oldest=now-100d earliest=now query="some text" index=nagios* limit=1000 field=message body="{
    \"size\": 10,
    \"query\": {
           \"filtered\": {
               \"query\": {
                   \"query_string\": {
                       \"query\": \"*\"
                   }
               }
           }
       }
    }"


  This example generates events drawn from the result of the query

  """
  server = Option(doc='', require=False, default="10.0.35.83")

  port = Option(doc='', require=False, default="9200")

  index = Option(doc='', require=False, default="*")

  q = Option(doc='', require=False, default="*")

  fields = Option(doc='', require=False, default="message")

  oldest = Option(doc='', require=False, default="now")

  earl = Option(doc='', require=False, default="now-100d")

  limit = Option(doc='', require=False, validate=validators.Integer(), default=10000)

  body = Option(doc='', require=False, default=None)

  timeout = Option(doc='', require=False, default=10)

  one = Option(doc='', require=False, default=False)

  def generate(self):

    #self.logger.debug('SimulateCommand: %s' % self)  # log command line

    config = self.get_configuration()

    #pp = pprint.PrettyPrinter(indent=4)
    self.logger.debug('Setup ES')
    es = Elasticsearch('{}:{}'.format(self.server, self.port), timeout=self.timeout)
    if not self.body:
        body = {
           "query": {
               "filtered": {
                   "query": {
                       "query_string": {
                           "query": self.q
                       }
                   }
               }
           }
        }
    else:
        body = self.body

    #pp.pprint(body);
    res = es.search(size=self.limit, index=self.index, body=body);

    # if response.status_code != 200:
    #   yield {'ERROR': results['error']['text']}
    #   return


    # date_time = '2014-12-21T16:11:18.419Z'
    # pattern = '%Y-%m-%dT%H:%M:%S.%fZ'

    if not self.one:
        for hit in res['hits']['hits']:
            yield self.getEvent(hit)
    else:
        if type(res) == list:
          for hit in res:
            yield self.getEvent(hit)
        elif type(res) == dict:
          yield self.getEvent(res)
        elif type(res) == unicode:
          for hit in res.split('\n'):
            yield self.getEvent(hit)
        else:
          yield self.getEvent(res)

  def getEvent(self, result):

    # hit["_source"][defaultField] = hit["_source"][defaultField].replace('"',' ');
    # epochTimestamp = hit['_source']['@timestamp'];
    # hit['_source']['_epoch'] = int(time.mktime(time.strptime(epochTimestamp, pattern)))
    # hit['_source']["_raw"]=hit['_source'][defaultField]

    if not self.one:
        event = {'_time': time.time(),
                 '_index': result['_index'],
                 '_type': result['_type'],
                 '_id': result['_id'],
                 '_score': result['_score'],
                 '_raw': json.dumps(result)
                }
    else:
        event = {
                '_time': time.time(),
                '_raw': json.dumps(result)
                }

    return event

  def get_configuration(self):
    sourcePath = os.path.dirname(os.path.abspath(__file__))
    config_file = open(sourcePath + '/config.json')
    return json.load(config_file)

  def __init__(self):
    super(GeneratingCommand, self).__init__()

dispatch(EsCommand, sys.argv, sys.stdin, sys.stdout, __name__)