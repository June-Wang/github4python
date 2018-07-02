#!/usr/bin/env python3

import datetime,sys,json,requests
#import sys

def make_json_data(scan_frequency):
    frequency=scan_frequency
    now = datetime.datetime.now()
    start = now - datetime.timedelta(minutes=frequency)

    start_time = start.strftime('%Y-%m-%d %H:%M:00.000')
    end_time = now.strftime('%Y-%m-%d %H:%M:00.000')
    #print(start_time,end_time)

    #start='2018-07-02 02:22:00.000'
    #end='2018-07-02 02:27:00.000'

    json_data ={
  "from": 0,
  "size": 150,
  "query": {
    "bool": {
      "must": {
        "query_string": {
          "query": "application_name:Oracle"
        }
      },
      "filter": {
        "bool": {
          "must": {
            "range": {
              "timestamp": {
                "from": start_time,
                "to": end_time
              }
            }
          }
        }
      }
    }
  },
  "sort": [
    {
      "timestamp": {
        "order": "desc"
      }
    }
  ]
}
    return(json_data)

def search(uri, json_data):
    """Simple Elasticsearch Query"""
    query = json.dumps(json_data)
    response = requests.get(uri, data=query)
    results = json.loads(response.text)
    return(results)

if __name__=="__main__":
    #print(make_json_data(15))
    json_data = make_json_data(600)
    uri="http://10.211.16.235:9200/_search?request_cache=true"
    results = search(uri, json_data)
    res = results['hits']['hits']
    #print(res)
    for i in range(len(res)):
        date = res[i]['_source']['timestamp']
        source = res[i]['_source']['source']
        message = res[i]['_source']['message']
        print(date,source,message)
