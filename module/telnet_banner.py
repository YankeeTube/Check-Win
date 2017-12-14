import requests

def http_banner():
    try:
        r = requests.get("http://localhost").headers
        if r.get("server"):
            banner = r.get("server")
        return banner
    except:
        banner = ""
if __name__ == '__main__':
    print(http_banner())