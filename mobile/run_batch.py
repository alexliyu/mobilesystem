#!/usr/bin/env python

import os, sys
from django.core.management import setup_environ
import settings
setup_environ(settings)

from batch_processing import run_batch

    
if __name__ == '__main__':
    run_batch(sys.argv[1], sys.argv[2], sys.argv[3], False)