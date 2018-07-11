#!/usr/bin/env python3

import csv,datetime,sys,re
import requests,dateparser
import mysql.connector
from mysql.connector import errorcode
from configparser import ConfigParser

def read_db_config(filename='config.ini', section='mysql'):
    """ Read database configuration file and return a dictionary object
    :param filename: name of the configuration file
    :param section: section of database configuration
    :return: a dictionary of database parameters
    """
    # create parser and read ini configuration file
    parser = ConfigParser()
    parser.read(filename)
 
    # get section, default to mysql
    db = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        raise Exception('{0} not found in the {1} file'.format(section, filename))
 
    return(db)

def con_mysql():

    db_config = read_db_config()
    #print(db_config)
    
    try:
        print('Connecting to MySQL database...')
        cnx = mysql.connector.connect(**db_config)
        if cnx.is_connected():
            print('Connection established.')
        else:
            print('Connection failed.')

    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
          print("Something is wrong with your user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
          print("Database does not exist")
      else:
          print(err)
    
    return(cnx)

def make_time_url(frequency):
    #frequency=1
    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(minutes=frequency)
    time_from = start_time.strftime('%Y-%m-%d %H:%M:00.000')
    time_to = end_time.strftime('%Y-%m-%d %H:%M:00.000')
    time_url = 'from=' + time_from + '&to=' + time_to + '&'
    time_url = time_url.replace(" ", "%20")
    time_url = time_url.replace(":", "%3A")
    return(time_url)

def get_csv_data(csv_url,user,passwd):
    with requests.Session() as s:
        download = s.get(csv_url,stream=True,auth=(user, passwd))
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        data_list = list(cr)
        #for row in data_list:
        #    print(row)
        return(data_list)

def get_all_data_list(data_list):
    request_re = re.compile('\?.+$')
    dup_re = re.compile('\/\/')
    #匹配多个条件
    ignore_re = re.compile("(^-|^API|^Java|-Monitor|yunjiankong|nagios|check_http|okhttp|HttpClient)")
    all_data_list = list()
    for data in data_list[1:]:
        agent = data[3]
        if re.search(ignore_re,agent):
            continue
        dt = dateparser.parse(data[0])
        try:
            #调整时区
            date = dt.astimezone().strftime('%Y-%m-%d %H:%M:%S')
        except:
            continue
        request = re.sub(request_re,'',data[1])
        url = re.sub(dup_re,'/',request)
        stat = data[2]
        row = (date,url,stat,agent)
        all_data_list.append(row)
    return(all_data_list)

if __name__=="__main__":
    graylog_url='http://graylog.server.local:9000/api/search/universal/absolute/export?'
    search_condition='query=nginx_version%3A1.6.x&'
    request_fields='fields=timestamp%2Crequest%2Cresponse%2Cagent%2CTIME&decorate=true'
    frequency = 1
    time_url = make_time_url(frequency)
    csv_url = graylog_url + search_condition + time_url + request_fields
    #print(csv_url)
    data_list = get_csv_data(csv_url,'view','readonly')
    all_data_list = get_all_data_list(data_list)
    #print(all_data_list)
    #sys.exit(0)
    cnx = con_mysql()
    cursor = cnx.cursor()
    query = ("INSERT INTO tbl_graylog_pv "
                      "(date, url, stat, agent) "
                      "VALUES (%s, %s, %s, %s)")

    try:
        cursor.executemany(query, all_data_list)
        cnx.commit()
        cursor.close()
    except mysql.connector.Error as err:
        print(err)

    finally:
        cnx.close()
        print('Connection closed.')
        print('Total:',str(len(all_data_list)))
