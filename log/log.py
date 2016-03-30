__author__ = 'xulei'
import logging

def InitLog():
    logging.basicConfig(
        level    = logging.DEBUG,
        format   = 'LINE %(lineno)-4d  %(levelname)-8s %(message)s',
        datefmt  = '%m-%d %H:%M',
        filename = 'autobuild.log',
        filemode = 'w')
    # define a Handler which writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    # set a format which is simpler for console use
    formatter = logging.Formatter('LINE %(lineno)-4d : %(levelname)-8s %(message)s')
    # tell the handler to use this format
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)