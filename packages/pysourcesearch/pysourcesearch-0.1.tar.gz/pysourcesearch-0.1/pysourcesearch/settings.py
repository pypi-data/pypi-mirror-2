from run import SETTINGS 

packages = {}

for package in SETTINGS['package_groups']:
    name, package = package.split(':')
    packages[name] = {
        'location' : package
    }
    
for desc in SETTINGS['package_descriptions']:
    name, desc = desc.split(':')
    packages[name]['description'] = desc
    