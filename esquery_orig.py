from __future__ import absolute_import, division, print_function, unicode_literals
import os, sys
import time
from time import sleep

splunkhome = '/opt/splunk'
sys.path.append(os.path.join(splunkhome, 'etc', 'apps', 'esquery_app', 'lib'))

#from cryptography.fernet import Fernet
#import cryptography.fernet as c
import splunk.Intersplunk as isp
import splunklib.results as results
import splunklib.client as client
from splunklib.searchcommands import dispatch, GeneratingCommand, Configuration, Option, validators

with open('/opt/splunk/etc/apps/esquery_app/Splunkey.bin', 'rb') as file_object:
    for line in file_object:
        key = line

with open('/opt/splunk/etc/apps/esquery_app/splunk_byte.bin', 'rb') as file_object:
    for line in file_object:
        cipher = line

#cipher_suite = c.Fernet(key)
HOST = "wlfeslinprd01.cyberleaf.io"
PORT = 8089
USERNAME = "kbryan"
#PASSWORD = bytes(cipher_suite.decrypt(cipher)).decode('utf-8')
PASSWORD = bytes(cipher).decode('utf-8')[10:21]


# searchquery = "| inputlookup append=T es_notable_events"
searchquery = str(sys.argv[1])
    
# Create a Service instance and log in 
service = client.connect(
    host=HOST,
    port=PORT,
    username=USERNAME,
    password=PASSWORD)


kwargs_normalsearch = {"exec_mode": "normal"}
job = service.jobs.create(searchquery, **kwargs_normalsearch)

# A normal search returns the job's SID right away, so we need to poll for completion
while True:
    while not job.is_ready():
        pass
    stats = {"isDone": job["isDone"],
              "doneProgress": float(job["doneProgress"])*100,
              "scanCount": int(job["scanCount"]),
              "eventCount": int(job["eventCount"]),
              "resultCount": int(job["resultCount"])}

    status = ("\r%(doneProgress)03.1f%%   %(scanCount)d scanned   "
              "%(eventCount)d matched   %(resultCount)d results") % stats

    # sys.stdout.write(status)
    # sys.stdout.flush()
    if stats["isDone"] == "1":
        # sys.stdout.write("\n\nDone!\n\n")
        break
    sleep(0.1)

# Get the results and display them
A = results.ResultsReader(job.results())
results = []
for result in A:
    results.append(result)
    # yield result

job.cancel()

isp.outputResults(results)