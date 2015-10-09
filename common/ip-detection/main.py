import ifconfig
import uptime
import communications

communications.updateData('Raspberry Pi ifconfig output', ifconfig.getIfconfigOutput())
communications.updateData('Raspberry Pi system uptime', uptime.getUptimeString())

print 'Success!'