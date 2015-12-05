#!/usr/bin/python
from wsgiref.handlers import CGIHandler
import pizza
import os

CGIHandler.os_environ = os.environ 
CGIHandler().run(pizza.app)

