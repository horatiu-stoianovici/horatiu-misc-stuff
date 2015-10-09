import commands

def getIfconfigOutput():
	return commands.getoutput('/sbin/ifconfig')
