from winreg import *
import platform
import sys
import nicinfo

def iis_Check():
    iis_subkey = "SOFTWARE\Microsoft\InetStp"
    reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    value = None
    try:
        iis_key = OpenKey(reg, iis_subkey)  # HKLM\SOFTWARE\Microsoft\InetStp
        for x in range(1024):
            try:
                enum = EnumValue(iis_key, x)
                if enum[0] == "MajorVersion":
                    value = enum[1]
                else:
                    value = ""
            except:
                pass
    except:
        value = None
    return value

def iis_version():
    iis_subkey = "SYSTEM\CurrentControlSet\Services\W3SVC\Parameters"
    reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    iis_value = None
    try:
        iis_key = OpenKey(reg, iis_subkey)  # HKLM\SYSTEM\CurrentControlSet\Services\W3SVC\Parameters
        for x in range(1024):
            try:
                enum = EnumValue(iis_key, x)
                if enum[0] == "MajorVersion":
                    iis_value = enum[1]
            except OSError:
                break
    except FileNotFoundError:
        pass
    return iis_value

def nic_Exist(reg,des,service):
    value = None
    for x in range(len(des)):
        try:
            if len(des) > 1 and len(service) > 1:
                if des[0] == des[1]:
                    del des[x]
                if service[0] == service[1]:
                    del service[x]
        except:
            pass
    subkey = "SYSTEM\CurrentControlSet\Services\\NetBT\Parameters\Interfaces" # SYSTEM\CurrentControlSet\Services\\NetBT\Parameters\Interfaces
    cnt = 0
    for x in range(1024):
        try:
            net_service_low = service[cnt].lower()
            net_service_up = service[cnt].upper()
            key = OpenKey(reg, subkey)
            enum = EnumKey(key,x)
            if enum == "Tcpip_{}".format(net_service_low) or enum == "Tcpip_{}".format(net_service_up):
                try:
                    subkey = "SYSTEM\CurrentControlSet\Services\\NetBT\Parameters\Interfaces\Tcpip_{}".format(net_service_low)  # SYSTEM\CurrentControlSet\Services\\NetBT\Parameters\Interfaces
                except:
                    subkey = "SYSTEM\CurrentControlSet\Services\\NetBT\Parameters\Interfaces\Tcpip_{}".format(net_service_up)  # SYSTEM\CurrentControlSet\Services\\NetBT\Parameters\Interfaces
                key = OpenKey(reg,subkey)
                value = EnumValue(key,1)
                cnt +=1
        except OSError:
            break
        except IndexError:
            break
    return value

def netBios_Bind_Service():
    subkey = "SOFTWARE\Microsoft\Windows NT\CurrentVersion\\NetworkCards"
    reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    des = []
    service = []
    for x in range(nicinfo.len_nic()):
        try:
            key = OpenKey(reg, subkey)  # SOFTWARE\Microsoft\Windows NT\CurrentVersion\\NetworkCards
            enum_key = EnumKey(key, x)
            subkey2 = subkey + "\\" + enum_key
            key2 = OpenKey(reg,subkey2)
            try:
                for y in range(1024):
                    enum = EnumValue(key2,y)
                    if enum[0] == "Description":
                        des.append(enum[1])
                    if enum[0] == "ServiceName":
                        service.append(enum[1])
            except OSError:
                continue
        except OSError:
            break
    if len(des) >= 1 and len(service) >=1:
        value = nic_Exist(reg,des,service)
    else:
        value = None
        return value
    return value[1]

def odbc():
    if "64bit" in platform.architecture():
        subkey = "SOFTWARE\ODBC\ODBC.INI"
    else:
        subkey = "SOFTWARE\Wow6432Node\ODBC\ODBC.INI"
    reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    try:
        key = OpenKey(reg, subkey)  # HKLM\SOFTWARE\Microsoft\InetStp
        for x in range(10):
            try:
                enum = EnumKey(key,x)
                if enum == "ODBC Data Sources":
                    value = enum
                    break
                else:
                    value = ""
            except:
                value = ""
    except:
        value = ""
    return value

def startup_program():
    subkey = "SOFTWARE\Microsoft\Windows\CurrentVersion\Run"
    reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    value = []
    try:
        key = OpenKey(reg, subkey)  # HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
        x = 0
        try:
            while True:
                enum = EnumValue(key, x)
                if enum[0] != '(기본값)':
                    value.append(enum[0])
                else:
                    value = ""
                x = x + 1
        except:
            pass
    except:
        value.append("")
    return value

def w07_registry():
    w07_subkey = "SYSTEM\CurrentControlSet\Control\Lsa"
    reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    w07_value = ""
    try:
        w07_key = OpenKey(reg,w07_subkey) # HKLM\SYSTEM\CurrentControlSet\Control\Lsa
        for x in range(1024):
            try:
                enum = EnumValue(w07_key,x)
                if enum[0] == "everyoneincludesanonymous":
                    w07_value = enum[1]
            except:
                pass
        CloseKey(w07_key)
    except FileNotFoundError:
        w07_value = ""

    return w07_value

def w13_registry():
    w13_subkey = "SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"
    reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    w13_value = None
    try:
        w13_key = OpenKey(reg, w13_subkey)  # HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System
        for x in range(1024):
            try:
                enum = EnumValue(w13_key, x)
                if enum[0] == "dontdisplaylastusername":
                    w13_value = enum[1]
            except:
                pass
        CloseKey(w13_key)
    except FileNotFoundError:
        w13_value = None
    return w13_value

def w20_registry():
    w20_subkey = "SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters"
    reg = ConnectRegistry(None,HKEY_LOCAL_MACHINE)
    w20_value = ""
    try:
        w20_key = OpenKey(reg,w20_subkey) # HKLM\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters
        for x in range(1024):
            try:
                enum = EnumKey(w20_key, x)
                if enum[0] == "AutoShareWks" or enum[0] == "AutoShareServer":
                    w20_value = enum[1]
            except OSError:
                w20_value = ""
        CloseKey(w20_key)
    except FileNotFoundError:
        w20_value = ""
    return w20_value

def w27_registry():
    w27_subkey = "SYSTEM\CurrentControlSet\Services\IISADMIN"
    reg = ConnectRegistry(None,HKEY_LOCAL_MACHINE)
    w27_value = False
    try:
        w27_key = OpenKey(reg, w27_subkey)  # HKLM\SYSTEM\CurrentControlSet\Services\IISADMIN
        for num in range(1024):
            try:
                enum = EnumValue(w27_key, num)
                if enum[0] == "ObjectName":
                    w27_value = enum[1]
                    break
                else:
                    w27_value = False
            except:
                pass
        CloseKey(w27_key)
    except FileNotFoundError:
        w27_value = False
    return w27_value

def w34_registry():
    w34_subkey = "SYSTEM\CurrentControlSet\Services\W3SVC\Parameters"
    reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    w34_value = ""
    try:
        w34_key = OpenKey(reg, w34_subkey)  # HKLM\SYSTEM\CurrentControlSet\Services\W3SVC\Parameters
        for x in range(1024):
            try:
                enum = EnumValue(w34_key, x)
                if enum[0] == "SSIEnableCmdDirective":
                    w34_value = enum[1]
                else:
                    w34_value = ""
            except:
                pass
        CloseKey(w34_key)
    except FileNotFoundError:
        w34_value = ""
    return w34_value

def w41_registry():
    w41_subkey = "SOFTWARE\Microsoft\Windows NT\CurrentVersion\DNS Server\Zones"
    reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    w41_values = {}
    w41_values2 = {}
    for n in range(1024):
        try:
            key = OpenKey(reg, w41_subkey)  # HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\DNS Server\Zones
            enum_key = EnumKey(key,n)
            new_subkey = w41_subkey + "\\" + enum_key
            CloseKey(key)
            try:
                w41_key = OpenKey(reg,new_subkey)
                for x in range(1024):
                    try:
                        enum = EnumValue(w41_key, x)
                        if enum[0] == "DatabaseFile":
                            # w41_values2.append(enum[1])
                            w41_values2['DatabaseFile'] = enum[1]
                        elif enum[0] == "SecureSecondaries":
                            # w41_values2.append(enum[1])
                            w41_values2['SecureSecondaries'] = enum[1]
                        elif enum[0] == "SecondaryServers":
                            # w41_values2.append(enum[1])
                            w41_values2['SecondaryServers'] = enum[1]
                    except OSError:
                        w41_values[enum_key] = w41_values2
                        break
                CloseKey(w41_key)
            except FileNotFoundError:
                pass
        except OSError:
            break
        except FileNotFoundError:
            break
    return w41_values

def w42_registry():
    w42_subkey = "System\CurrentControlSet\Services\W3SVC\Parameters\ADCLaunch"
    reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    flag = False
    try:
        OpenKey(reg,w42_subkey) # HKLM\System\CurrentControlSet\Services\W3SVC\Parameters\ADCLaunch
        flag = True
    except:
        pass
    return flag

def w44_registry():
    w44_subkey = "SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp"
    reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    w44_value = None
    try:
        w44_key = OpenKey(reg, w44_subkey)  # HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp
        for x in range(1024):
            try:
                enum = EnumValue(w44_key, x)
                if enum[0] == "MinEncryptionLevel":
                    w44_value = enum[1]
            except:
                pass
        CloseKey(w44_key)
    except FileNotFoundError:
        w44_value = None
    return w44_value

def w47_registry():
    result = None
    try:
        w47_subkey = "SYSTEM\CurrentControlSet\Services\SNMP\Parameters\ValidCommunities"
        reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
        w47_key = OpenKey(reg,w47_subkey) # HKLM\SYSTEM\CurrentControlSet\Services\SNMP\Parameters\ValidCommunities
        try:
            for x in range(1024):
                enum = EnumValue(w47_key, x)
                result = enum
        except OSError:
            if len(result) < 1:
                result = None
    except FileNotFoundError:
        result = None
    return result

def w48_registry():
    w48_subkey = "SYSTEM\CurrentControlSet\Services\SNMP\Parameters\PermittedManagers"
    reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    w48_value = None
    try:
        w48_key = OpenKey(reg, w48_subkey)  # HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp
        for x in range(1024):
            try:
                enum = EnumValue(w48_key, x)
                if enum[1] == "localhost":
                    continue
                else:
                    w48_value = enum[1]
            except OSError:
                break
        CloseKey(w48_key)
    except FileNotFoundError:
        w48_value = None
    return w48_value

def w49_registry():
    w49_subkey = "SOFTWARE\Microsoft\Windows NT\CurrentVersion\DNS Server\Zones"
    reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    w49_value = None
    try:
        w49_key = OpenKey(reg, w49_subkey)  # HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\DNS Server\Zones
        for x in range(1024):
            try:
                enum = EnumValue(w49_key, x)
                if enum[1] == "AllowUpdate":
                    w49_value = enum[0]
            except OSError:
                break
        CloseKey(w49_key)
    except FileNotFoundError:
        w49_value = None
    return w49_value

def w51_registry():
    w51_subkey = "Software\Microsoft\TelnetServer\\1.0\SecurityMechanism"
    reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    w51_value = None
    try:
        w51_key = OpenKey(reg, w51_subkey)  # HKLM\Software\Microsoft\TelnetServer\1.0\SecurityMechanism
        for x in range(1024):
            try:
                enum = EnumValue(w51_key, x)
                if enum[0] == "SecurityMechanism":
                    w51_value = enum[1]
            except OSError:
                break
        CloseKey(w51_key)
    except FileNotFoundError:
        w51_value = None
    return w51_value

def w53_registry():
    version_list = ["10","8.1","8","7","2016","2012"]
    if platform.release() in version_list:
        w53_subkey = "SOFTWARE\Policies\Microsoft\Windows NT\Terminal Services" # New Version (Windows 7 이후 모델)
        reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
        w53_value = False
        w53_values = {}
        try:
            w53_key2 = OpenKey(reg, w53_subkey)  # HKLM\SOFTWARE\Policies\Microsoft\Windows NT\Terminal Services
            for x in range(1024):
                try:
                    enum = EnumValue(w53_key2, x)
                    if enum[0] == "MaxIdleTime":
                        w53_values['MaxIdleTime'] = enum[1] # KiSA 원격 터미널 접속 타임아웃은 세션 유휴시간만을 보기때문에 아래 2개는 안봄
                    # elif enum[0] == "MaxDisconnectionTime":
                    #     w53_values['MaxDisconnectionTime'] = enum[1]
                    # elif enum[0] == "MaxConnectionTime":
                    #     w53_values['MaxConnectionTime'] = enum[1]
                except OSError:
                    if len(w53_values) > 1:
                        w53_value = True
                    break
            CloseKey(w53_key2)
        except FileNotFoundError:
            w53_value = False
        return w53_value,w53_values
    else:
        w53_subkey = "SYSTEM\ControlSet001\Control\Terminal Server\WinStations\RDP-Tcp"  # Rectangle Version (구형 버전 / 2008 이전 모델)
        w53_subkey2 = "SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp"  # Rectangle Version (구형 버전 / 2008 이전 모델)
        reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
        w53_value = False
        w53_values = []
        try:
            w53_key = OpenKey(reg, w53_subkey2)  # HKLM\SYSTEM\ControlSet001\Control\Terminal Server\WinStations\RDP-Tcp
            for x in range(1024):
                try:
                    enum = EnumValue(w53_key, x)
                    if enum[0] == "fEnableWinStation":
                        if enum[1] == 1:
                            w53_value = True
                except OSError:
                    break
            CloseKey(w53_key)
        except FileNotFoundError:
            w53_value = None
        try:
            w53_key2 = OpenKey(reg, w53_subkey2)  # HKLM\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp
            for x in range(1024):
                try:
                    enum = EnumValue(w53_key2, x)
                    if enum[0] == "MaxIdleTime":
                        w53_values['MaxIdleTime'] = enum[1]
                    # elif enum[0] == "MaxDisconnectionTime":
                    #     w53_values['MaxDisconnectionTime'] = enum[1]
                    # elif enum[0] == "MaxConnectionTime":
                    #     w53_values['MaxConnectionTime'] = enum[1]
                except OSError:
                    if len(w53_values) > 1:
                        w53_value = True
                    break
            CloseKey(w53_key2)
        except FileNotFoundError:
            w53_value = False
        return w53_value,w53_values

def w60_registry():
    w60_application = []
    w60_security = []
    w60_system = []
    try:
        w60_subkey = "SYSTEM\CurrentControlSet\Services\Eventlog\Application"
        reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
        w60_key = OpenKey(reg, w60_subkey)  # HKLM\SYSTEM\CurrentControlSet\Services\Eventlog\Application
        for x in range(1024):
            try:
                enum = EnumValue(w60_key, x)
                if enum[0] == "MaxSize":
                    w60_application.append(enum[1])
                elif enum[0] == 'AutoBackupLogFiles':
                    w60_application.append(enum[1])
            except OSError:
                break
        CloseKey(w60_key)
    except FileNotFoundError:
        pass

    try:
        w60_subkey = "SYSTEM\CurrentControlSet\Services\EventLog\Security"
        reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
        w60_key = OpenKey(reg, w60_subkey)  # HKLM\SYSTEM\CurrentControlSet\Services\Eventlog\Security
        for x in range(1024):
            try:
                enum = EnumValue(w60_key, x)
                if enum[0] == "MaxSize":
                    w60_security.append(enum[1])
                elif enum[0] == 'AutoBackupLogFiles':
                    w60_security.append(enum[1])
            except OSError:
                break
        CloseKey(w60_key)
    except FileNotFoundError:
        pass

    try:
        w60_subkey = "SYSTEM\CurrentControlSet\Services\Eventlog\System"
        reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
        w60_key = OpenKey(reg, w60_subkey)  # HKLM\SYSTEM\CurrentControlSet\Services\Eventlog\System
        for x in range(1024):
            try:
                enum = EnumValue(w60_key, x)
                if enum[0] == "MaxSize":
                    w60_system.append(enum[1])
                elif enum[0] == 'AutoBackupLogFiles':
                    w60_system.append(enum[1])
            except OSError:
                break
        CloseKey(w60_key)
    except FileNotFoundError:
        pass



    return w60_application,w60_security,w60_system

def w64_registry():
    w64_values = []
    w64_subkey = "Control Panel\Desktop"
    reg = ConnectRegistry(None, HKEY_CURRENT_USER)
    try:
        w60_key = OpenKey(reg, w64_subkey)  # HKCU\Control Panel\Desktop
        for x in range(1024):
            try:
                enum = EnumValue(w60_key, x)
                if enum[0] == "ScreenSaveActive":
                    w64_values.append(enum[1])
                elif enum[0] == 'ScreenSaverIsSecure':
                    w64_values.append(enum[1])
                elif enum[0] == 'ScreenSaveTimeOut':
                    w64_values.append(enum[1])
            except OSError:
                break
        CloseKey(w60_key)
    except FileNotFoundError:
        pass
    return w64_values

def w65_registry():
    w65_value = None
    w65_subkey = "SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System"
    reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    try:
        w65_key = OpenKey(reg, w65_subkey)  # HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System
        for x in range(1024):
            try:
                enum = EnumValue(w65_key, x)
                if enum[0] == "shutdownwithoutlogon":
                    w65_value = enum[1]
            except OSError:
                break
        CloseKey(w65_key)
    except FileNotFoundError:
        w65_value = None
    return w65_value

def w68_registry():
    w68_subkey = "SYSTEM\CurrentControlSet\Control\Lsa"
    w68_value = None
    reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    try:
        w68_key = OpenKey(reg, w68_subkey)  # HKLM\SYSTEM\CurrentControlSet\Control\Lsa
        for x in range(1024):
            try:
                enum = EnumValue(w68_key, x)
                if enum[0] == "restrictanonymous":
                    w68_value = enum[1]
            except OSError:
                break
        CloseKey(w68_key)
    except FileNotFoundError:
        w68_value = None
    return w68_value

def w69_registry():
    w69_value = None
    w69_subkey = "Software\Microsoft\Windows NT\CurrentVersion\Winlogon"
    reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    try:
        w69_key = OpenKey(reg, w69_subkey)  # HKLM\Software\Microsoft\Windows NT\CurrentVersion\Winlogon
        for x in range(1024):
            try:
                enum = EnumValue(w69_key, x)
                if enum[0] == "AutoAdminLogon":
                    w69_value = enum[1]
            except OSError:
                break
        CloseKey(w69_key)
    except FileNotFoundError:
        w69_value = None
    return w69_value

def w72_registry():
    w72_values = []
    version = platform.release()
    vulner_ver = ["NT","2003","95","2008","98","2000","ME"]
    if version in vulner_ver:
        w72_subkey = "System\CurrentControlSet\Services\Tcpip\Parameters"
        reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
        try:
            w72_key = OpenKey(reg, w72_subkey)  # HKLM\System\CurrentControlSet\Services\Tcpip\Parameters
            for x in range(1024):
                try:
                    enum = EnumValue(w72_key, x)
                    if enum[0] == "SynAttackProtect":
                        w72_values.append(enum[1])
                    elif enum[0] == "EnableDeadGWDetect":
                        w72_values.append(enum[1])
                    elif enum[0] == "KeepAliveTime":
                        w72_values.append(enum[1])
                    elif enum[0] == "NoNameReleaseOnDemand":
                        w72_values.append(enum[1])
                except OSError:
                    break
            CloseKey(w72_key)
        except FileNotFoundError:
            pass
    return w72_values

def w74_registry():
    w74_values = {}
    w74_subkey = "System\CurrentControlSet\Services\LanManServer\Parameters"
    reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    try:
        w74_key = OpenKey(reg, w74_subkey)  # HKLM\System\CurrentControlSet\Services\LanManServer\Parameters
        for x in range(1024):
            try:
                enum = EnumValue(w74_key, x)
                if enum[0] == "EnableForcedLogoff":
                    w74_values["EnableForcedLogoff"] = enum[1]
                elif enum[0] == "AutoDisconnect":
                    w74_values["AutoDisconnect"] = enum[1]
            except OSError:
                break
        CloseKey(w74_key)
    except FileNotFoundError:
        pass

    return w74_values

def w75_registry():
    w75_values = {}
    w75_subkey = "SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon"

    reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    try:
        w75_key = OpenKey(reg, w75_subkey)  # HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon
        for x in range(1024):
            try:
                enum = EnumValue(w75_key, x)
                if enum[0] == "LegalNoticeCaption":
                    w75_values["LegalNoticeCaption"] = enum[1]
                elif enum[0] == "LegalNoticeText":
                    w75_values["LegalNoticeText"] = enum[1]
            except OSError:
                break
        CloseKey(w75_key)
    except FileNotFoundError:
        pass

    return w75_values

def w82_registry():
    w82_value = None
    w82_subkey = "Software\Microsoft\Microsoft SQL Server"
    reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    try:
        w82_key = OpenKey(reg, w82_subkey)  # HKLM\Software\Microsoft\Microsoft SQL Server
        for x in range(1024):
            try:
                enum = EnumKey(w82_key, x)
                if "MSSQL" in enum:
                    w82_subkey2 = w82_subkey + "\\" + enum
                    w82_key2 = OpenKey(reg,w82_subkey2)
                    try:
                        for y in range(1024):
                            enum2 = EnumKey(w82_key2,y)
                            if enum2 == "MSSQLServer":
                                w82_subkey3 = w82_subkey2 + "\\" + enum2
                                w82_key3 = OpenKey(reg,w82_subkey3)
                                for z in range(1024):
                                    enum_val = EnumValue(w82_key3,z)
                                    if enum_val[0] == "LoginMode":
                                        w82_value = enum_val[1]
                                        break
                    except OSError:
                        pass
            except OSError:
                break
        CloseKey(w82_key)
    except FileNotFoundError:
        w82_value = None
    return w82_value

if __name__ == '__main__':
    print(netBios_Bind_Service())