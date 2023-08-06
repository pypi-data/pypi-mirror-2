#!/usr/bin/env python
#
# Service Activation Engine
#
import os,sys,site

if __name__ == '__main__':
    # Adjust paths
    d=os.path.dirname(sys.argv[0])
    if not d:
        d=os.getcwd()
    d=os.path.abspath(os.path.join(d,".."))
    contrib=os.path.abspath(os.path.join(d,"contrib","lib"))
    sys.path.insert(0,contrib)
    sys.path.insert(0,os.path.abspath(os.path.join(d,"..")))
    sys.path.insert(0,d)
    # Install eggs from contrib/lib
    site.addsitedir(contrib)
    # Check settings.py
    try:
        import settings
    except ImportError:
        sys.stderr.write("Error: Can't find file 'settings.py'. (If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n")
        sys.exit(1)
    os.environ['DJANGO_SETTINGS_MODULE']="noc.settings"
    # Run SAE
    from noc.sa.sae import SAE
    sae=SAE()
    sae.process_command()
