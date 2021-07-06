import sys
import os
import subprocess
import re
import time
from datetime import datetime
from esquery_helper import login
import rsa

def suppress(source,dest,src,dt,suppress_time=24,run="yes"):
    
    suppress_time = int(suppress_time)
    if dest=='null':
        dest = '*'
        dest_search = 'NOT (dest="{}" OR dest_ip="{}")'.format(dest,dest)
    
    else:
        dest_search = '(dest="{}" OR dest_ip="{}")'.format(dest,dest)
    
    if src=='null':
        src = '*'
        src_search = 'NOT (src="{}" OR src_ip="{}")'.format(src,src)
    
    else:
        src_search = '(src="{}" OR src_ip="{}")'.format(src,src)
    
    if run.lower()=="yes":
        utc = dt.split('T')[0]
        utc = time.strptime(utc,'%Y-%m-%d')
        Time = int(time.mktime(utc))
        Time_end = int(Time+3600*suppress_time)
        # Read Eventtypes file to ensure no duplicates
        # Get event types file
        
        with open('/opt/splunk/etc/apps/SA-ThreatIntelligence/local/eventtypes.conf','r') as f:
            text = f.read()
        eventtypes = re.findall('\[.*\]',text)
        eventname = 'notable_suppression-'+source
        
        if eventname in eventtypes:
            i = 1
            new_eventname = eventname+'_{}'.format(i)
            while new_eventname in eventtypes:
                i+=1
                new_eventname = eventname+'_{}'.format(i)
        
        else:
            new_eventname = eventname.replace(' ','_')
        
        contents1,contents2 = login()
        
        curl_statement = '''curl -k -u {} https://localhost:8089/servicesNS/nobody/SA-ThreatIntelligence/saved/eventtypes -d name="{}_Test" -d search='`get_notable_index` source="{}" {} {} _time>={} _time<={}\''''.format(rsa.decrypt(contents1,contents2).decode(),new_eventname,source,dest_search,src_search,Time,Time_end)
        
        # args = ['curl', '-k', '-u', '{}'.format(rsa.decrypt(contents1,contents2).decode())]
        # args += ['https://localhost:8089/servicesNS/nobody/SA-ThreatIntelligence/saved/eventtypes','-d']
        # split_str = '''name="{}_Test" -d search="`get_notable_index` source='{}' dest='{}' src='{}' _time>={}"'''.format(new_eventname,source,dest,src,Time).replace('`','\`').split(' ')
        # for split in split_str:
        #     args.append(split)
        
        # subprocess.Popen(args)
        os.system(curl_statement)
    
if __name__=='__main__':
    
    source = ' '.join(sys.argv[1:-5])
    dest = sys.argv[-5]
    src = sys.argv[-4]
    dt = sys.argv[-3]
    suppress_time = sys.argv[-2]
    run = sys.argv[-1]
    suppress(source,dest,src,dt,suppress_time,run)