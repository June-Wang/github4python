#!/usr/bin/env python3

import re,sys,datetime
from elasticsearch import Elasticsearch

title = str(sys.argv[1])
es_index = str(sys.argv[2])
#time = datetime.datetime.now()
time = datetime.datetime.utcnow()
date_now = time.strftime('%Y-%m-%d')
es = Elasticsearch()
bodys = bodys = {
  "query": {
    "bool": {
      "must": [
        { "match": { "level":   "ERROR"        }}
      ],
      "filter": {
       "range": {
      "@timestamp": {
      "gte": "now-6m",
      "lt": "now"
      }
        }
    }
    }
  }
}

try:
    res = es.search(index=es_index, body=bodys)
except:
    print(es_index+' is not found!')
    sys.exit(0)
#print("Got %d Hits:" % res['hits']['total'])
#ignore_re = re.compile('nkp-listener')
#ignore_re_msg = re.compile(': timeout')

#error_msg = {}
error_list = []
total = 0
for hit in res['hits']['hits']:
#    if (re.search(ignore_re,hit["_source"]['module']) and re.search(ignore_re_msg,hit["_source"]['message'])):
#        continue
    if hit["_source"]['level'] == 'ERROR':
        err_msg = str("%(host)s %(module)s %(level)s: %(message)s" % hit["_source"])
        #err_msg = hit["_source"]['message']
        #err_module = hit["_source"]['module']
        error_list.append(err_msg)
        total += 1

if total > 0:
    stats = 'WARNING'
    print('total: '+ str(total))
    for msg in sorted(error_list):
        print(msg)
    print('|'+"error="+ str(total))
    sys.exit(1)
else:
    stats = 'OK'
    print(title+" is OK.| error=0")
    sys.exit(0)
