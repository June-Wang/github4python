#!/usr/bin/env python3

import datetime,sys,json,requests

def make_json_data(scan_frequency):
    frequency=scan_frequency
    now = datetime.datetime.utcnow()
    #now = datetime.datetime.now()
    start = now - datetime.timedelta(minutes=frequency)

    start_time = start.strftime('%Y-%m-%d %H:%M:00.000')
    end_time = now.strftime('%Y-%m-%d %H:%M:00.000')
    #print(start_time,end_time)

    #start='2018-07-02 02:22:00.000'
    #end='2018-07-02 02:27:00.000'

    json_data = {
  "from": 0,
  "size": 150,
  "query": {
    "bool": {
      "must": {
        "query_string": {
          "query": "nginx_access:true",
        }
      },
      "filter": {
        "bool": {
          "must": [
            {
              "range": {
                "timestamp": {
                  "from": start_time,
                  "to": end_time,
                }
              }
            },
            {
              "query_string": {
                "query": "streams:547b29b6d4c6c10b4f1b934d"
              }
            }
          ]
        }
      }
    }
  }
}
    return(json_data)

def search(uri, json_data):
    """Simple Elasticsearch Query"""
    query = json.dumps(json_data)
    response = requests.get(uri, data=query)
    results = json.loads(response.text)
    return(results)

if __name__=="__main__":
    json_data = make_json_data(1)
    print(json_data)
    uri="http://10.211.16.236:9200/_search?request_cache=true"
    results = search(uri, json_data)
    #print(results)
    res = results['hits']['hits']
    #print(res)
    total = len(res)
    if total == 0:
        print('results is empty.')
        sys.exit(1)
    for i in range(total):
        #date = res[i]['_source']['timestamp']
        #source = res[i]['_source']['source']
        #message = res[i]['_source']['message']
        #print(date,source,message)
        print(res[i]['_source'])
    print('Total:',str(total))
