# Splunk API Processes

# Implementation of various processes using the Splunk REST API as opposed to
# modifying files manually.

import os
import sys
import subprocess
from Users_Auth import create_role, create_app, auth
from Clients_Dict import clients_info as CI
from cryptography.fernet import Fernet


# Add lookup table file to lookups folder from lookup staging area
def updateLookup(appName,appFile,lookupFile):
    
    os.system('curl -k -u {} https://localhost:8089/servicesNS/nobody/{}/data/lookup-table-files/{} -d eai:data=/opt/splunk/var/run/splunk/lookup_tmp/{}'.format(bytes(auth()[1].decrypt(auth()[0])).decode('utf-8'),appName,appFile,lookupFile))

# Delete lookup table file
# Make sure to end lookupName with file format (ex: .csv)
def deleteLookup(appName,lookupName):
    
    os.system('curl -k -u {} --request DELETE https://localhost:8089/servicesNS/nobody/{}/data/lookup-table-files/{}'.format(bytes(auth()[1].decrypt(auth()[0])).decode('utf-8'),appName,lookupName))
