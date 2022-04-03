from pysnmp.hlapi import *

def consultaSNMP(comunidad,host,oid):
    errorIndication, errorStatus, errorIndex, varBinds = next(
        getCmd(SnmpEngine(),
               CommunityData(comunidad),
               UdpTransportTarget((host, 161)),
               ContextData(),
               ObjectType(ObjectIdentity(oid))))

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        for varBind in varBinds:
            varB=(' = '.join([x.prettyPrint() for x in varBind]))
            return varB
        #print(varB)

def consultaSNMPW(comunidad,host,oid):
    for(errorIndication,
        errorStatus,
        errorIndex,
        varBinds) in nextCmd(SnmpEngine(),
                            CommunityData(comunidad),
                            UdpTransportTarget((host,161)),
                            ContextData(),
                            ObjectType(ObjectIdentity(oid)),
                            lexicographicMode=False
                            ):
        if errorIndication:
            print("Error",errorIndication)
        elif errorStatus:
            print("Error",'%s at %s' % (errorStatus.prettyPrint(),errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            for varBind in varBinds:
                varB=(' = '.join([x.prettyPrint() for x in varBind]))
                resultado= varB.split()[2]
            print(varB)


#res = consultaSNMP('comunidadASR','192.168.0.12','1.3.6.1.2.1.1.4.0')
#consultaSNMP('comunidadASR','192.168.0.112','1.3.6.1.2.1.6.13.1.1')



res = consultaSNMPW('comunidadASR','192.168.0.112','1.3.6.1.2.1.6.13.1.1')
print(res)