import sys
import os
import subprocess
import re
import time
from datetime import datetime
from esquery_helper import login
import rsa

def suppress(rule_name,dest,src):
    
    utc = datetime.utcnow()
    Time = int(time.mktime(datetime(utc.year,utc.month,utc.day).timetuple()))
    # Read Eventtypes file to ensure no duplicates
    # Get event types file
    
    with open('/opt/splunk/etc/apps/SA-ThreatIntelligence/local/eventtypes.conf','r') as f:
        text = f.read()
    eventtypes = re.findall('\[.*\]',text)
    eventname = 'notable_suppression-'+rule_name
    
    if eventname in eventtypes:
        i = 1
        new_eventname = eventname+'_{}'.format(i)
        while new_eventname in eventtypes:
            i+=1
            new_eventname = eventname+'_{}'.format(i)
    
    else:
        new_eventname = eventname
    
    contents1,contents2 = login()
    
    curl_statement = '''curl -k -u {} https://localhost:8089/servicesNS/nobody/SA-ThreatIntelligence/saved/eventtypes -d name="{}_Test" -d search="`get_notable_index` source='{}' dest='{}' src='{}' _time>={}"'''.format(rsa.decrypt(contents1,contents2).decode(),new_eventname,rule_name,dest,src,Time).replace('`','\`')
    
    # args = ['curl', '-k', '-u', '{}'.format(rsa.decrypt(contents1,contents2).decode())]
    # args += ['https://localhost:8089/servicesNS/nobody/SA-ThreatIntelligence/saved/eventtypes','-d']
    # split_str = '''name="{}_Test" -d search="`get_notable_index` source='{}' dest='{}' src='{}' _time>={}"'''.format(new_eventname,rule_name,dest,src,Time).replace('`','\`').split(' ')
    # for split in split_str:
    #     args.append(split)
    
    # subprocess.Popen(args)
    os.system(curl_statement)
    
if __name__=='__main__':
    
    rule_name = sys.argv[1]
    dest = sys.argv[2]
    src = sys.argv[3]
    with open('/opt/splunk/etc/apps/esquery_app/bin/File.txt','w') as f:
            pass        
    suppress(rule_name,dest,src)