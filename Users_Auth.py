# Functions for Users and Authentication in Splunk

import os
# import sys
from cryptography.fernet import Fernet
import subprocess
from Clients_Dict import clients_dict

def auth():
    with open('/root/API/Splunk_Key.bin','rb') as f:
        for line in f:
            k = line
    
    with open('/root/API/Splunk_Cred.bin','rb') as f:
        for line in f:
            c = line
            
    sp1 = subprocess.Popen('uname -r', shell=True, stdout=subprocess.PIPE)
    
    sp2 = subprocess.Popen('cat /etc/os-release', shell=True, stdout=subprocess.PIPE)
    
    sp3 = subprocess.Popen('hostnamectl', shell=True, stdout=subprocess.PIPE)
    
    cs = Fernet(k+sp1.stdout.read()+sp2.stdout.read()+sp3.stdout.read())
    
    return c, cs

# Get Abbreviations for Clients
# Create a role by editing the /$SPLUNK_HOME/etc/system/local/authorize.conf
def create_role(clientName,clientAbbrev):
    
    capabilities = ['list_accelerate_search','list_inputs','run_collect',
                    'run_mcollect','schedule_rtsearch','search']
    indexes = ['_internal','{}_*'.format(clientAbbrev.lower()),'notable','notable_summary']
    command_str = 'curl -k -u {} https://localhost:8089/services/authorization/roles -d name={}_user -d cumulativeRTSrchJobsQuota=0 -d cumulativeSrchJobsQuota=0 -d defaultApp={}_dashboards'.format(bytes(auth()[1].decrypt(auth()[0])).decode('utf-8'),clientName.lower(),clientName.lower())
    
    for c in capabilities:
        command_str+=' -d capabilities={}'.format(c)
    
    for i in indexes:
        command_str+=' -d srchIndexesAllowed={}'.format(i)
    
    os.system(command_str)


def create_app(clientName,clientAbbrev,appTemplate):
    
    os.system('curl -k -u {} https://localhost:8089/services/apps/local -d name={}_dashboards -d template={}'.format(bytes(auth()[1].decrypt(auth()[0])).decode('utf-8'),clientName,appTemplate))