version = '1.3.2'
release = True
revision = 'dev'

if release:
    fullVersion = '%s' % (version,)
else:
    fullVersion = '%s-%s' % (version, revision)
    
titleVersion = 'Version %s' % (fullVersion,)
