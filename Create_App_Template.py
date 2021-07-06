# Transform Client Application into a template
import os
import sys
import time
import re
from Clients_Dict import clients_df

template_dir = '/opt/splunk/share/splunk/app_templates/client_template/'
SplunkName = 'arctos'
dashboard_dir = '/opt/splunk/etc/apps/{}_dashboards/'.format(SplunkName)
configFile_def = os.path.join(dashboard_dir,'default','app.conf')


def AppConfigTemp(configFile='/opt/splunk/share/splunk/app_templates/client_template/default/app.conf',
                  clientName='Arctos', 
                  tempDest='/opt/splunk/share/splunk/app_templates/client_template/default/app.conf'):
    
    with open(configFile,'r') as f:
        contents = f.read()
    
    # Put the client name in the file
    newContents = contents.replace(clientName, '[clientName]')
    with open(tempDest,'w') as f:
        f.write(newContents)


def DefaultNavTemp(navFile='/opt/splunk/share/splunk/app_templates/client_template/local/data/ui/nav/default.xml',
                   officialName='Arctos',splunkName='arctos', 
                   tempDest='/opt/splunk/share/splunk/app_templates/client_template/local/data/ui/nav/default.xml'):
    
    with open(navFile,'r') as f:
        contents = f.read()
    
    newContents = contents.replace(officialName, 'CLIENTNAME').\
        replace(splunkName, 'clientname')
    
    with open(tempDest,'w') as f:
        f.write(newContents)


def AssetReportingTemp(reportingFile='/opt/splunk/share/splunk/app_templates/client_template/local/data/ui/views/arctos_asset_reporting.xml',
                       AssetFile='arctos_assets.csv', officialName='Arctos',
                       tempDest='/opt/splunk/share/splunk/app_templates/client_template/local/data/ui/views/template_asset_reporting.xml'):
    
    with open(reportingFile,'r') as f:
        contents = f.read()
    
    newContents = contents.replace(officialName, '[ClientName]').\
        replace(AssetFile, '[AssetFile]')
    
    with open(tempDest,'w') as f:
        f.write(newContents)
    
    os.system('rm {}'.format(reportingFile))


def OverviewTemp(overviewFile='/opt/splunk/share/splunk/app_templates/client_template/local/data/ui/views/arctos_overview.xml',
                 officialName='Arctos',splunkName='arctos',ClientAbbrev='arc', AssetFile='arctos_assets.csv',
                 tempDest='/opt/splunk/share/splunk/app_templates/client_template/local/data/ui/views/template_overview.xml'):
    
    with open(overviewFile,'r') as f:
        contents = f.read()
        
    newContents = contents.replace(officialName, '[ClientName]').\
        replace('>'+splunkName+'<', '>[ClientNameLower]<').\
            replace('>'+ClientAbbrev+'<', '>[ClientAbbrev]<').\
                replace(AssetFile, '[AssetFile]')
    
    with open(tempDest,'w') as f:
        f.write(newContents)
    
    os.system('rm {}'.format(overviewFile))


def TransformsTemp(transformsFile='/opt/splunk/share/splunk/app_templates/client_template/local/transforms.conf',
                   splunkName='arctos',tempDest='/opt/splunk/share/splunk/app_templates/client_template/local/transforms.conf'):
    
    with open(transformsFile,'r') as f:
        contents = f.read()
        
    newContents = contents.replace(splunkName.lower(), '[clientname]')
    
    with open(tempDest,'w') as f:
        f.write(newContents)


def MetaTemp(metaFile='/opt/splunk/share/splunk/app_templates/client_template/metadata/local.meta',
             splunkName='arctos', tempDest='/opt/splunk/share/splunk/app_templates/client_template/metadata/local.meta'):
    

    with open(metaFile,'r') as f:
        contents = f.read()
    
    newContents = contents.replace(splunkName.lower(), '[clientname]')
    
    with open(tempDest,'w') as f:
        f.write(newContents)


def app_to_template(officialName='Arctos'):
    
    clientName = officialName.lower()
    # os.system('cd /opt/splunk/share/splunk/app_templates/')
    # os.system('find ./client_template/ -type > dirs.txt')
    
    # Rename existing application template and create a new one.
    os.system('mv /opt/splunk/share/splunk/app_templates/client_template /opt/splunk/share/splunk/app_templates/client_template_'+str(int(time.time())))
    
    # os.system('xargs mkdir -p < dirs.txt')
    # os.system('rm dirs.txt')
    
    
    # Copy files to client_template folder
    os.system('cp -r /opt/splunk/etc/apps/{}/. /opt/splunk/share/splunk/app_templates/client_template'.format(officialName+'_dashboards'))
    os.system('rm -r /opt/splunk/share/splunk/app_templates/client_template/lookups/*')
    
    clientAbbrev = clients_df.loc[clientName.lower()]['abbrev']
    officialName = clients_df.loc[clientName.lower()]['official_name']
    splunkName = clientName.lower().replace(' ','')
    assetFile = splunkName+'_assets.csv'
    
    AppConfigTemp(configFile='/opt/splunk/share/splunk/app_templates/client_template/default/app.conf',
                  clientName=officialName, 
                  tempDest='/opt/splunk/share/splunk/app_templates/client_template/default/app.conf')
    
    DefaultNavTemp(navFile='/opt/splunk/share/splunk/app_templates/client_template/local/data/ui/nav/default.xml',
                   officialName=officialName,splunkName=splunkName, 
                   tempDest='/opt/splunk/share/splunk/app_templates/client_template/local/data/ui/nav/default.xml')
    
    AssetReportingTemp(reportingFile='/opt/splunk/share/splunk/app_templates/client_template/local/data/ui/views/arctos_asset_reporting.xml',
                       AssetFile=assetFile, officialName=officialName,
                       tempDest='/opt/splunk/share/splunk/app_templates/client_template/local/data/ui/views/template_asset_reporting.xml')
    
    OverviewTemp(overviewFile='/opt/splunk/share/splunk/app_templates/client_template/local/data/ui/views/arctos_overview.xml',
                 officialName=officialName,splunkName=splunkName,ClientAbbrev=clientAbbrev, AssetFile=assetFile,
                 tempDest='/opt/splunk/share/splunk/app_templates/client_template/local/data/ui/views/template_overview.xml')
    
    TransformsTemp(transformsFile='/opt/splunk/share/splunk/app_templates/client_template/local/transforms.conf',
                   splunkName=splunkName,tempDest='/opt/splunk/share/splunk/app_templates/client_template/local/transforms.conf')
    
    MetaTemp(metaFile='/opt/splunk/share/splunk/app_templates/client_template/metadata/local.meta',
             splunkName=splunkName, tempDest='/opt/splunk/share/splunk/app_templates/client_template/metadata/local.meta')
    
    os.system('chmod -R 777 /opt/splunk/share/splunk/app_templates/client_template')

if __name__=='__main__':
    
    args = sys.argv
    clientName = args[1]
    
    app_to_template(clientName)