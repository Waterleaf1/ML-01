# Create Splunk Apps and modify them

import os
import sys
import time
import re
from Users_Auth import create_role, create_app
from Clients_Dict import clients_df

def CreateApp(appName,appTemplate,clientName,splunkName,clientAbbrev):
    
    ClientID = clients_df.loc[clientName.lower(),'id']
    
    # Create App using Splunk's REST API
    create_app(splunkName,clientAbbrev,appTemplate)
    
    
    # Change filename from the template filenames
    os.system('mv /opt/splunk/etc/apps/{}/local/data/ui/views/template_asset_reporting.xml'.format(appName.lower())+
              ' /opt/splunk/etc/apps/{}/local/data/ui/views/{}_asset_reporting.xml'.format(appName.lower(),splunkName))
    
    os.system('mv /opt/splunk/etc/apps/{}/local/data/ui/views/template_overview.xml'.format(appName.lower())+
              ' /opt/splunk/etc/apps/{}/local/data/ui/views/{}_overview.xml'.format(appName.lower(),splunkName))
    
    create_role(splunkName,clientAbbrev)
    
    try:
        os.system('python3 /root/API/Client_Assets.py {}'.format(ClientID))
        
    except Exception as e:
        print(e)
    

def EditAppConfig(clientName,configFile):
    
    with open(configFile,'r') as f:
        contents = f.read()
    
    # Put the client name in the file
    newContents = contents.replace('[clientName]',clientName)
    with open(configFile,'w') as f:
        f.write(newContents)
    
    
# Edit Default file in Nav folder
def EditDefaultNav(clientName,splunkName,navFile):
    
    with open(navFile,'r') as f:
        contents = f.read()
    
    newContents = contents.replace('CLIENTNAME',clientName).replace('clientname',splunkName)
    
    with open(navFile,'w') as f:
        f.write(newContents)


# Edit Deployment Assets Dashboard
def EditAssetReporting(ClientName='Arctos',AssetFile='arctos_assets.csv',reportingFile='/opt/splunk/etc/apps/arctos_dashboards/local/data/ui/views/arctos_asset_reporting.xml'):
    
    with open(reportingFile,'r') as f:
        contents = f.read()
    
    newContents = contents.replace('[ClientName]',ClientName).replace('[AssetFile]',AssetFile)
    
    with open(reportingFile,'w') as f:
        f.write(newContents)


# Take an Overview Dashboard and create a template by replacing Client-Specific parts
# ClientName should be like the official capitalization for the organization
# def CreateOverveiwTemplate(ClientName,clientAbbrev,overviewFile):
    
#     with open(overviewFile,'r') as f:
#         contents = f.read()
        
#     newContents = contents.replace(ClientName,'[ClientName]').replace(ClientName.lower(),'[clientname]').replace(' '+clientAbbrev.lower()+'_',' [clientabbrev]_')
    
#     with open(overviewFile,'w') as f:
#         f.write(newContents)


# Edit Overview Dashboard
def EditOverview(ClientName='Arctos',splunkName='arctos',ClientAbbrev='arc',AssetFile='arctos_assets.csv',overviewFile='/opt/splunk/etc/apps/arctos_dashboards/local/data/ui/views/arctos_overview.xml'):
    
    with open(overviewFile,'r') as f:
        contents = f.read()
        
    newContents = contents.replace('[ClientName]',ClientName).replace('[ClientNameLower]',splunkName).replace('[ClientAbbrev]',ClientAbbrev).replace('[AssetFile]',AssetFile)
    
    with open(overviewFile,'w') as f:
        f.write(newContents)
        

def EditTransforms(clientName,transformsFile):
    
    with open(transformsFile,'r') as f:
        contents = f.read()
        
    newContents = contents.replace('[clientname]',clientName.lower())
    
    with open(transformsFile,'w') as f:
        f.write(newContents)
    
    
def EditMeta(splunkName,metaFile):
    
    create_time = time.time()
    with open(metaFile,'r') as f:
        contents = f.read()
    
    newContents = contents.replace('[clientname]',splunkName.lower())
    
    # Get splunk version from splunk.version file
    with open('/opt/splunk/etc/splunk.version','r') as f:
        line = f.readline()
        if 'version' in line.lower():
            splunk_version = line.lower().replace('=',' = ').replace('\n','')
            
    newContents = re.sub('version = (.*)',splunk_version,newContents)
    newContents = re.sub('modtime = (.*)','modtime = {}'.format(create_time),newContents)
    with open(metaFile,'w') as f:
        f.write(newContents)
    
    
if __name__=='__main__':
    
    args = sys.argv
    clientName = args[1]
    clientAbbrev = clients_df.loc[clientName.lower()]['abbrev']
    officialName = clients_df.loc[clientName.lower()]['official_name']
    splunkName = clientName.lower().replace(' ','')
    assetFile = splunkName+'_assets.csv'
    appName = '{}_dashboards'.format(splunkName)
    appTemplate = 'client_template'
    CreateApp(appName,appTemplate,clientName,splunkName,clientAbbrev)
    
    configFile = '/opt/splunk/etc/apps/{}/default/app.conf'.format(appName)
    EditAppConfig(officialName,configFile)
    
    navFile = '/opt/splunk/etc/apps/{}/local/data/ui/nav/default.xml'.format(appName)
    EditDefaultNav(officialName,splunkName,navFile)
    
    reportingFile = '/opt/splunk/etc/apps/{}/local/data/ui/views/{}_asset_reporting.xml'.format(appName,splunkName)
    EditAssetReporting(officialName,assetFile,reportingFile)
    
    overviewFile = '/opt/splunk/etc/apps/{}/local/data/ui/views/{}_overview.xml'.format(appName,splunkName)
    EditOverview(officialName,splunkName,clientAbbrev,assetFile,overviewFile)
    
    transformsFile = '/opt/splunk/etc/apps/{}/local/transforms.conf'.format(appName)
    EditTransforms(splunkName,transformsFile)
    
    metaFile = '/opt/splunk/etc/apps/{}/metadata/local.meta'.format(appName)
    EditMeta(splunkName,metaFile)