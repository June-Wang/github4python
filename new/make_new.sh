#!/bin/bash

./newone.py |\
awk -F',' '/^[0-9]/{print "tushare_lite,ts_code="$1" trade_date="$2",pct_chg="$3",pct_chg_3d="$4",pct_chg_5d="$5",pct_chg_10d="$6",pct_chg_20d="$7",pct_chg_30d="$8",pct_chg_60d="$9",pct_chg_90d="$10",avg_w="$11",close="$(NF-3)",weight="$(NF-2)",vol="$(NF-1)" "$NF}'
