#!/usr/bin/python
import sys
import logging 
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/home/hoclab/http/c4aengines")
from main import app as application
