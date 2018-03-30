#!/usr/bin/env python3

import sys
import time
import numpy as np
import pandas as pd
#from sqlalchemy import create_engine
import mysql.connector
from mysql.connector import errorcode

config = {
  'user': 'query',
  'password': 'query',
  'host': '10.1.1.101',
  'database': 'bfb',
  'raise_on_warnings': True,
}

try:
  cnx = mysql.connector.connect(**config)
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)

cursor = cnx.cursor()

pv_stat_query=("select stat,url,count(*) as sum "
"from tbl_bfb_pv "
"where stat = %s and date >=DATE_SUB(CURRENT_DATE, INTERVAL 1 DAY) and "
"date < CURRENT_DATE group by url "
"order by sum DESC limit %s;")

stat_list = [499,404]
top = 10
data_list = list()

for stat in stat_list:
    cursor.execute(pv_stat_query,(stat,top))
    for (stat,url,count) in cursor:
        if count >= 10:
            data_list.append([stat,url,count])

cursor.close()
cnx.close()

#print(np.vstack(my_list))
df = pd.DataFrame(np.vstack(data_list),columns=['状态','URL','数量'])
s = df.style.set_properties(**{'background-color': '#D2D8F9',
                           'color': '#000000',
                           'border-color': 'white'}).render()
#print(s.to_html(index=False))
print(s)
