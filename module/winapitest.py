from netifaces import AF_INET, AF_INET6, AF_LINK
import netifaces
interface_list = netifaces.interfaces()
# interface = filter(lambda x: 'eth' in x,interface_list)
print(interface_list)