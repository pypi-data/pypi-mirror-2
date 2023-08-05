# PySNMP SMI module. Mostly autogenerated from
# smidump -f python SNMP-FRAMEWORK-MIB
# by libsmi2pysnmp-0.0.8-alpha at Tue Feb  5 16:09:21 2008,
# Python version (2, 4, 4, 'final', 0)

try:
    import socket
    import os
except ImportError:
    pass
import string
import time

# Imported just in case new ASN.1 types would be created
from pyasn1.type import constraint, namedval

# Imports

( Integer, ObjectIdentifier, OctetString, ) = mibBuilder.importSymbols("ASN1", "Integer", "ObjectIdentifier", "OctetString")
( ModuleCompliance, ObjectGroup, ) = mibBuilder.importSymbols("SNMPv2-CONF", "ModuleCompliance", "ObjectGroup")
( Bits, Integer32, ModuleIdentity, MibIdentifier, ObjectIdentity, MibScalar, MibTable, MibTableRow, MibTableColumn, TimeTicks, snmpModules, ) = mibBuilder.importSymbols("SNMPv2-SMI", "Bits", "Integer32", "ModuleIdentity", "MibIdentifier", "ObjectIdentity", "MibScalar", "MibTable", "MibTableRow", "MibTableColumn", "TimeTicks", "snmpModules")
( TextualConvention, ) = mibBuilder.importSymbols("SNMPv2-TC", "TextualConvention")

# Types

class SnmpAdminString(TextualConvention, OctetString):
    displayHint = "255t"
    subtypeSpec = OctetString.subtypeSpec+constraint.ValueSizeConstraint(0,255)

class SnmpEngineID(OctetString, TextualConvention):
    subtypeSpec = OctetString.subtypeSpec+constraint.ValueSizeConstraint(5,32)
    try:
        # Attempt to base engine ID on local IP address
        defaultValue = '\x80\x00\x4f\xb8' + '\x05' + string.join(
            map(lambda x: chr(int(x)),
                string.split(socket.gethostbyname(socket.gethostname()),'.')),
            ''
            ) + chr(os.getpid() >> 8) + chr(os.getpid() & 0xff)
    except:
        # ...otherwise, use rudimentary text ID
        defaultValue = '\x80\x00\x4f\xb8' + '\x05'
        t = int(time.time())
        while t:
            defaultValue = defaultValue + chr(t & 0xff)
            t = t >> 8
            
class SnmpEngineTime(Integer32):
    def clone(self, value=None, tagSet=None, subtypeSpec=None):
        if value is None and self._value is not None:
            value = int(time.time())-self._value
        return Integer32.clone(self, value, tagSet, subtypeSpec)

class SnmpMessageProcessingModel(Integer32):
    subtypeSpec = Integer32.subtypeSpec+constraint.ValueRangeConstraint(0,2147483647L)

class SnmpSecurityLevel(Integer):
    subtypeSpec = Integer.subtypeSpec+constraint.SingleValueConstraint(1,3,2,)
    namedValues = namedval.NamedValues(("noAuthNoPriv", 1), ("authNoPriv", 2), ("authPriv", 3), )

class SnmpSecurityModel(Integer32):
    subtypeSpec = Integer32.subtypeSpec+constraint.ValueRangeConstraint(0,2147483647L)

# Objects

snmpFrameworkMIB = ModuleIdentity((1, 3, 6, 1, 6, 3, 10)).setRevisions(("2002-10-14 00:00","1999-01-19 00:00","1997-11-20 00:00",))
if mibBuilder.loadTexts: snmpFrameworkMIB.setOrganization("SNMPv3 Working Group")
if mibBuilder.loadTexts: snmpFrameworkMIB.setContactInfo("WG-EMail:   snmpv3@lists.tislabs.com\nSubscribe:  snmpv3-request@lists.tislabs.com\n\nCo-Chair:   Russ Mundy\n            Network Associates Laboratories\npostal:     15204 Omega Drive, Suite 300\n            Rockville, MD 20850-4601\n            USA\nEMail:      mundy@tislabs.com\nphone:      +1 301-947-7107\n\nCo-Chair &\nCo-editor:  David Harrington\n            Enterasys Networks\npostal:     35 Industrial Way\n            P. O. Box 5005\n            Rochester, New Hampshire 03866-5005\n            USA\nEMail:      dbh@enterasys.com\nphone:      +1 603-337-2614\n\nCo-editor:  Randy Presuhn\n            BMC Software, Inc.\npostal:     2141 North First Street\n            San Jose, California 95131\n            USA\nEMail:      randy_presuhn@bmc.com\nphone:      +1 408-546-1006\n\nCo-editor:  Bert Wijnen\n            Lucent Technologies\npostal:     Schagen 33\n            3461 GL Linschoten\n            Netherlands\n\n\n\nEMail:      bwijnen@lucent.com\nphone:      +31 348-680-485\n  ")
if mibBuilder.loadTexts: snmpFrameworkMIB.setDescription("The SNMP Management Architecture MIB\n\nCopyright (C) The Internet Society (2002). This\nversion of this MIB module is part of RFC 3411;\nsee the RFC itself for full legal notices.")
snmpFrameworkAdmin = MibIdentifier((1, 3, 6, 1, 6, 3, 10, 1))
snmpAuthProtocols = ObjectIdentity((1, 3, 6, 1, 6, 3, 10, 1, 1))
if mibBuilder.loadTexts: snmpAuthProtocols.setDescription("Registration point for standards-track\nauthentication protocols used in SNMP Management\nFrameworks.")
snmpPrivProtocols = ObjectIdentity((1, 3, 6, 1, 6, 3, 10, 1, 2))
if mibBuilder.loadTexts: snmpPrivProtocols.setDescription("Registration point for standards-track privacy\nprotocols used in SNMP Management Frameworks.")
snmpFrameworkMIBObjects = MibIdentifier((1, 3, 6, 1, 6, 3, 10, 2))
snmpEngine = MibIdentifier((1, 3, 6, 1, 6, 3, 10, 2, 1))
snmpEngineID = MibScalar((1, 3, 6, 1, 6, 3, 10, 2, 1, 1), SnmpEngineID()).setMaxAccess("readonly")
if mibBuilder.loadTexts: snmpEngineID.setDescription("An SNMP engine's administratively-unique identifier.\n\nThis information SHOULD be stored in non-volatile\nstorage so that it remains constant across\nre-initializations of the SNMP engine.")
snmpEngineBoots = MibScalar((1, 3, 6, 1, 6, 3, 10, 2, 1, 2), Integer32().subtype(subtypeSpec=constraint.ValueRangeConstraint(1, 2147483647L))).setMaxAccess("readonly")
if mibBuilder.loadTexts: snmpEngineBoots.setDescription("The number of times that the SNMP engine has\n(re-)initialized itself since snmpEngineID\nwas last configured.")
snmpEngineTime = MibScalar((1, 3, 6, 1, 6, 3, 10, 2, 1, 3), SnmpEngineTime().subtype(subtypeSpec=constraint.ValueRangeConstraint(0, 2147483647L))).setMaxAccess("readonly").setUnits("seconds")
if mibBuilder.loadTexts: snmpEngineTime.setDescription("The number of seconds since the value of\nthe snmpEngineBoots object last changed.\nWhen incrementing this object's value would\ncause it to exceed its maximum,\nsnmpEngineBoots is incremented as if a\nre-initialization had occurred, and this\nobject's value consequently reverts to zero.")
snmpEngineMaxMessageSize = MibScalar((1, 3, 6, 1, 6, 3, 10, 2, 1, 4), Integer32().subtype(subtypeSpec=constraint.ValueRangeConstraint(484, 2147483647L))).setMaxAccess("readonly")
if mibBuilder.loadTexts: snmpEngineMaxMessageSize.setDescription("The maximum length in octets of an SNMP message\nwhich this SNMP engine can send or receive and\nprocess, determined as the minimum of the maximum\nmessage size values supported among all of the\ntransports available to and supported by the engine.")
snmpFrameworkMIBConformance = MibIdentifier((1, 3, 6, 1, 6, 3, 10, 3))
snmpFrameworkMIBCompliances = MibIdentifier((1, 3, 6, 1, 6, 3, 10, 3, 1))
snmpFrameworkMIBGroups = MibIdentifier((1, 3, 6, 1, 6, 3, 10, 3, 2))

# Augmentions

# Groups

snmpEngineGroup = ObjectGroup((1, 3, 6, 1, 6, 3, 10, 3, 2, 1)).setObjects(("SNMP-FRAMEWORK-MIB", "snmpEngineID"), ("SNMP-FRAMEWORK-MIB", "snmpEngineBoots"), ("SNMP-FRAMEWORK-MIB", "snmpEngineMaxMessageSize"), ("SNMP-FRAMEWORK-MIB", "snmpEngineTime"), )

# Exports

# Module identity
mibBuilder.exportSymbols("SNMP-FRAMEWORK-MIB", PYSNMP_MODULE_ID=snmpFrameworkMIB)

# Types
mibBuilder.exportSymbols("SNMP-FRAMEWORK-MIB", SnmpAdminString=SnmpAdminString, SnmpEngineID=SnmpEngineID, SnmpEngineTime=SnmpEngineTime, SnmpMessageProcessingModel=SnmpMessageProcessingModel, SnmpSecurityLevel=SnmpSecurityLevel, SnmpSecurityModel=SnmpSecurityModel)

# Objects
mibBuilder.exportSymbols("SNMP-FRAMEWORK-MIB", snmpFrameworkMIB=snmpFrameworkMIB, snmpFrameworkAdmin=snmpFrameworkAdmin, snmpAuthProtocols=snmpAuthProtocols, snmpPrivProtocols=snmpPrivProtocols, snmpFrameworkMIBObjects=snmpFrameworkMIBObjects, snmpEngine=snmpEngine, snmpEngineID=snmpEngineID, snmpEngineBoots=snmpEngineBoots, snmpEngineTime=snmpEngineTime, snmpEngineMaxMessageSize=snmpEngineMaxMessageSize, snmpFrameworkMIBConformance=snmpFrameworkMIBConformance, snmpFrameworkMIBCompliances=snmpFrameworkMIBCompliances, snmpFrameworkMIBGroups=snmpFrameworkMIBGroups)

# Groups
mibBuilder.exportSymbols("SNMP-FRAMEWORK-MIB", snmpEngineGroup=snmpEngineGroup)
