import sys
import os

splunkhome = '/opt/splunk'
sys.path.append(os.path.join(splunkhome, 'etc', 'apps', 'esquery_app', 'lib'))

import rsa

def login():
    
    with open('/opt/splunk/etc/apps/esquery_app/bin/esquery_key1.txt', 'rb') as file_object:
        contents1 = file_object.read()
    
    with open('/opt/splunk/etc/apps/esquery_app/esquery_key2.pem', 'rb') as file_object:
        contents2 = rsa.PrivateKey.load_pkcs1(file_object.read())
    
    return contents1, contents2