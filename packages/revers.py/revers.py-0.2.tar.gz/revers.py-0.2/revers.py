#!/usr/bin/env python
#
# $Id: revers.py,v 405e2623bd27 2010/06/09 12:14:31 vsevolod $
#

from sys import argv
from reverstorm import revers

if __name__ == '__main__':
    
    if len(argv) != 2:
        print \
        """usage: revers.py <dburi>
where <dburi> like postgres://user:password@host/database
  then create ./models/*.py files, ./models/ must be exist
  warning!!! exists .py files in ./models/ are replaced
"""
        exit(1)

    revers(argv[1])
