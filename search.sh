#!/bin/bash

cat ./500.list|xargs -i ./search_new.py '{}' >> output.info
