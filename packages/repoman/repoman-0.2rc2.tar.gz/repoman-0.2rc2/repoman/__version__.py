major = '0.2'
minor = ''
tag = 'rc2'
revision = ''
version = major

if minor:
    version += '.' + minor
if tag:
    version += tag
if revision:
    version += '-r' + revision

