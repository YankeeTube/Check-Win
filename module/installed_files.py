from winreg import *

def installed_filename():
    result = []
    subkey = "SOFTWARE\Microsoft\Windows\CurrentVersion\\Uninstall"
    reg = ConnectRegistry(None,HKEY_LOCAL_MACHINE)
    try:
        key = OpenKey(reg,subkey) # HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall
        value = ""
        x = 0
        while True:
            enum = EnumKey(key,x)
            new_key = OpenKey(reg,subkey+"\\"+enum)
            try:
                y = 0
                while True:
                    new_enum = EnumValue(new_key,y)
                    if new_enum[0] == "DisplayName":
                        value = value +"\n"+ new_enum[1]
                        result.append(new_enum[1])
                        x = x+1
                        break
                    else:
                        y = y+1
                        continue
                x = x+1
            except:
                x = x+1
    except:
        pass
    return result

def SOFTWARE():
    result = []
    subkey = "SOFTWARE\WOW6432Node"
    reg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
    try:
        key = OpenKey(reg, subkey)  # HKLM\SOFTWARE\WOW6432Node
        value = ""
        x = 0
        while True:
            enum = EnumKey(key, x)
            value = value +"\n" + enum
            result.append(enum)
            x = x+1
    except:
        pass
    return result

def comp_ab():
    a = SOFTWARE()
    b = installed_filename()
    x = 0
    value = ""
    while True:
        if b[x] in a[x]:
            del b[x]
            x = x + 1
        elif b not in a:
            for y in range(len(b)):
                a.append(b[y])
            for z in range(len(a)):
                value = value +"\n" +a[z]
            break
        else:
            continue
    return value

if __name__ == '__main__':
    print(comp_ab())

