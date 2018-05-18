#!/usr/bin/env python3

import tushare as ts

try:
    df = ts.get_today_all()
except:
    print('get_today_all timeout!')
    sys.exit(1)

persent_all = 0
for persent in df.changepercent.values:
    if persent > 0:
        persent_all +=1
    if persent < 0:
        persent_all -=1

number_of_stock = len(df.changepercent.values)
now_status = int(float(persent_all)/float(number_of_stock)*100)

print("")
print(str(now_status))
