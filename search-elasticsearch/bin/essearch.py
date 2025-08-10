#!/usr/bin/env python3
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

import sys
import time
import json
from elasticsearch import Elasticsearch

from splunklib.searchcommands import \
    dispatch, GeneratingCommand, Configuration, Option, validators

@Configuration()
class EsCommand(GeneratingCommand):
    """ Generates events that are the result of a query against Elasticsearch

    ##Syntax

    .. code-block::
        es index=<string> | q=<string> | fields=<string> | oldest=<string> | earl=<string> | limit=<int>

    ##Description

    The :code:`es` issue a query to ElasticSearch, where the
    query is specified in :code:`q`.

    ##Example

    .. code-block::
        | es oldest=now-100d earliest=now query="some text" index=nagios* limit=1000 field=message

    This example generates events drawn from the result of the query

    """

    index = Option(doc='', require=False, default="*")
    q = Option(doc='', require=True)
    fields = Option(doc='', require=False, default="message")
    oldest = Option(doc='', require=False, default="now")
    earl = Option(doc='', require=False, default="now-1d")
    limit = Option(doc='', require=False, validate=validators.Integer(), default=100)

    def generate(self):
        self.logger.debug('Starting ES search command.')

        es = Elasticsearch()

        query = {
            "query_string": {
                "query": self.q
            }
        }

        try:
            res = es.search(
                index=self.index,
                query=query,
                size=self.limit
            )

            for hit in res['hits']['hits']:
                yield self.get_event(hit)

        except Exception as e:
            self.logger.error("Error during Elasticsearch search: %s", e)
            # You might want to yield an error event to Splunk
            yield {'_raw': f"Error during Elasticsearch search: {e}"}

    def get_event(self, result):
        event = {
            '_time': time.time(),
            '_index': result['_index'],
            '_type': result.get('_type', ''), # _type is deprecated
            '_id': result['_id'],
            '_score': result['_score'],
            '_raw': json.dumps(result)
        }
        return event

if __name__ == "__main__":
    dispatch(EsCommand, sys.argv, sys.stdin, sys.stdout, __name__)