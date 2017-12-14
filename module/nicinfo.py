import os
import re

def len_nic():
    a = os.popen("chcp 437 | netsh interface show interface")
    b = a.read()
    a.close()
    enable = re.search(re.compile("Enabled"),b).group()
    result = b.count(enable)
    return result