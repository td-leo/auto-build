__author__ = 'xulei'

from sql.sql import sql

from jenkin.jobs import jobs
from log.log import InitLog

def doBuild():
    sqlite = sql()
    job = jobs()

    job.Build(sqlite)

if __name__ == '__main__':
    InitLog()
    doBuild()
