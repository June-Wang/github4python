#!/usr/bin/env python3

import sys
import re
import os
import datetime
import time
import tushare as ts
import pandas as pd
import numpy as np

now = datetime.date.today()
date_time = now.strftime('%Y-%m-%d')

data_index = str(now.strftime('%Y%m%d'))+code
