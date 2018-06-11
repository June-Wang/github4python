#!/usr/bin/env python3

import sys
import datetime
import time
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

def get_day_all():
    try:
        #print('Get Day All...')
        df = ts.get_today_all()
    except:
        print('ts.get_today_all failed.')
        sys.exit(1)
    return(df)

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
    df = get_day_all()
    
    now = datetime.datetime.now()
    date_time = now.strftime('%Y-%m-%d %H:%M:%S')
    sys.exit(1)

    cnx = con_mysql()
    cursor = cnx.cursor()
    
    query = ("INSERT INTO tbl_sh_persent "
                      "(date, persent) "
                      "VALUES (%s, %s)")
    data = list()    
    persent_all = 0
    for persent in df.changepercent.values:
        if persent > 0:
            persent_all +=1
        else:
            persent_all -=1

    number_of_stock = len(df.changepercent.values)
    perent = int(float(persent_all)/float(number_of_stock)*100)
    row = (date_time,perent)
    data.append(row)

    try:
        cursor.executemany(query, data)    
        cnx.commit()
        cursor.close()
    except mysql.connector.Error as err:
        print(err)

    finally:
        cnx.close()
        print('Connection closed.')

if __name__ == '__main__':
    main()
