#!/usr/bin/env python
'''
Script will connect to each domain and update a Contact Record

Required python libraries:
    - Google gdata: http://code.google.com/apis/gdata/
'''

from storm.locals import *
import gdata.apps.service