#!/bin/bash

./go.py |\
awk -F',' '/^[0-9]/{print "tushare_lite,ts_code="$1" trade_date="$2",pct_chg="$3",pct_chg_3d="$4",pct_chg_5d="$5",pct_chg_10d="$6",pct_chg_20d="$7",pct_chg_30d="$8",pct_chg_60d="$9",pct_chg_90d="$10",close="$11",weight="$12",vol="$13",vol_chg_1d="$14",vol_avg_3d="$15",vol_chg_5d="$16" "$NF}'

#ts_code,trade_date,pct_chg,pct_chg_3d,pct_chg_5d,pct_chg_10d,pct_chg_20d,pct_chg_30d,pct_chg_60d,pct_chg_90d,close,weight,vol,vol_chg_1d,vol_avg_3d,vol_avg_5d,timestamp
