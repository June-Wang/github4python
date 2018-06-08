#!/usr/bin/env python3

import sys
import datetime
import tushare as ts
import mysql.connector
from mysql.connector import errorcode
#from mysql.connector import MySQLConnection, Error
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

def get_pe_data():
    try:
        print('Get Stock Basics...')
        df_pe = ts.get_stock_basics()
    except:
        print('Get Stock Basics failed.')
        sys.exit(1)
    return(df_pe)

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

def main():
    df_pe = get_pe_data()
    
    now = datetime.date.today()
    date_time = now.strftime('%Y-%m-%d')
    index_time = now.strftime('%Y%m%d')

    cnx = con_mysql()
    cursor = cnx.cursor()
    
    query_pe = ("INSERT INTO tbl_pe_day "
                      "(id, date, code, pe) "
                      "VALUES (%s, %s, %s, %s)")
    data_pe = list()    
    for code in df_pe.index:
        id = index_time + code
        date = date_time
        pe = int(df_pe[df_pe.index == code]['pe'][0])
        row = (id,date,code,pe)
        data_pe.append(row)
    #print(data_pe)
    try:
        cursor.executemany(query_pe, data_pe)    
        cnx.commit()
        cursor.close()
    except mysql.connector.Error as err:
        print(err)

    finally:
        cnx.close()
        print('Connection closed.')

if __name__ == '__main__':
    main()
