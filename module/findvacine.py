from winreg import *
import os



def windows_defender():
    subkey = "SOFTWARE\Microsoft\Windows Defender\Signature Updates"
    reg = ConnectRegistry(None,HKEY_LOCAL_MACHINE)
    try:
        key = OpenKey(reg,subkey) # HKLM\SOFTWARE\Microsoft\Windows Defender\Signature Updates
        x = 0
        while True:
            enum = EnumValue(key, x)
            if enum[0] =="EngineVersion":
                value = enum[1]
                break
            else:
                x = x+1
                value = ""
    except:
        value = ""
    return value

# def v3():
#     result = "V3 제품군은 제작사에서 엔진 버전을 비공개하며, 제품구매자에게만 열람이 가능합니다. [수동점검]"
#     return result
#
if __name__ == '__main__':
    a = windows_defender()
    print(a)
