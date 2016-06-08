#!/bin/bash

grep -oP 'data-code=\"\d{6}\"' ./n*.html|awk -F'"' '{print $(NF-1)}'|sort -u > nxx.list
