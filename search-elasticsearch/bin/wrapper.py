import os, sys
import logging
import subprocess
import splunk.Intersplunk 
 
## LOGGING ###
LOG_FILENAME = '/tmp/wrappery.py.log'
#create logger
logger = logging.getLogger("wrapper")
logger.setLevel(logging.DEBUG)
#create file handler and set level to debug
fh = logging.FileHandler(LOG_FILENAME)
fh.setLevel(logging.DEBUG)
#create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s -  %(message)s")
#add formatter to ch and fh
fh.setFormatter(formatter)
#add ch and fh to logger
logger.addHandler(fh)
logger.debug('========Wrapper=========')


### DELETING ENV VARS ###
# Remove problematic environmental variables if they exist.
for envvar in ("PYTHONPATH", "LD_LIBRARY_PATH"):
    if envvar in os.environ:
        del os.environ[envvar]
        
logger.debug("env vars unset")


### USING OS INTERPRETER ###
python_executable = "/usr/bin/python"
try:
  real_script = os.path.join(os.path.dirname(__file__), "search.py")
  p = subprocess.Popen([python_executable, real_script]+ sys.argv[1:] , stdout=subprocess.PIPE,  stderr=subprocess.PIPE)
  out, err = p.communicate()
  print out
  splunk.Intersplunk.outputResults(out); 
except:
  for l in sys.exc_info():
    logger.debug(l);
  logger.debug("END");
