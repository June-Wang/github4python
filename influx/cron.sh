#!/bin/bash

start_time=`date -d now +"%F"|xargs -r -i echo "{} 09:46"|xargs -r -i date -d "{}" +"%s"`
end_time=`date -d now +"%F"|xargs -r -i echo "{} 15:00"|xargs -r -i date -d "{}" +"%s"`

end_min=`date -d now +"%F %H:%M:56"|xargs -r -i date -d "{}" +"%s"`
my_now=`date -d now +"%s"`

day_week=`date -d now +"%u"`
[ ${day_week} -gt 5 ] && exit

num=`echo "(${my_now} - ${start_time}) < 0"|bc`
[ "${num}" == '1' ] && exit
num=`echo "(${my_now} - ${end_time}) > 0"|bc`
[ "${num}" == '1' ] && exit
num=`echo "(${my_now} - ${end_min}) > 0"|bc`
[ "${num}" == '1' ] && exit

while true
do
    my_now=`date -d now +"%s"`
    num=`echo "(${my_now} - ${end_min}) > 0"|bc`
    [ "${num}" == '1' ] && exit
    /bin/bash /home/wangxj/github4python/influx/coll_stock.sh
    sleep 5s
done
