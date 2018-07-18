import string
import os
from sys import argv

script, arg1, arg2 = argv
os.system('python config-all/configtx.py ' + arg1)
os.system('python config-all/cryptoconfig.py ' + arg1)
os.system('python config-all/docker-compose-peer-n.py ' + arg1)
os.system('python config-all/howtobuildterraform.py ' + arg1)
os.system('python config-all/howtorevert.py ' + arg1)
os.system('python config-all/peeradmincard.py ' + arg1)
os.system('python config-all/startFabric-peer-n.py ' + arg1)