import sys

# simple way to centalize the logging and allow to log out to console for debugging
def log_debug(log, message):
    log.debug(message)
    #print(message, file=sys.stderr)
     
