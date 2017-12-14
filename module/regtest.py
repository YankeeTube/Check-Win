from winreg import *
keyVal = r"Software\WOW6432Node"
aKey = OpenKey(HKEY_LOCAL_MACHINE, keyVal, 0, KEY_ALL_ACCESS)
subkey = []
sub2key = []
try:
    i = 0
    while True:
        asubkey = EnumKey(aKey, i)
        print(asubkey)
        keyVal = keyVal +"\\"+ asubkey # HKLM\SOFTWARE\WOW6432Node\ + asubkey
        bKey = OpenKey(HKEY_LOCAL_MACHINE,keyVal,0,KEY_ALL_ACCESS)
        try:
            x = 0
            while True:
                if subkey and sub2key:
                    try:
                        cKey = OpenKey(HKEY_LOCAL_MACHINE,keyVal+"\\"+subkey[x-1]+"\\"+sub2key[x-1],0,KEY_ALL_ACCESS)
                        csubkey = EnumKey(cKey,x-1)
                        print(csubkey)
                    except:
                        sub2key = []
                        continue
                else:
                    asubkey = EnumKey(bKey,x)
                    if asubkey:
                        subkey.append(asubkey)
                        print(asubkey)
                        try:
                            bKey = OpenKey(HKEY_LOCAL_MACHINE,keyVal+"\\"+subkey[x],0,KEY_ALL_ACCESS)
                            bsubkey = EnumKey(bKey,x)
                            print(bsubkey)
                            sub2key.append(bsubkey)
                            x = x + 1
                        except:
                            pass

        except:
            pass
        i += 1
except WindowsError:
    pass