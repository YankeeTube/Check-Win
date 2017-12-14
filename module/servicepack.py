import re
import os
import platform
import requests
from lxml import html


def ms_os_version(table_num):
    r = requests.get("https://winrelinfo.blob.core.windows.net/winrelinfo/ko-KR.html")
    parser = html.fromstring(r.content)
    release = parser.xpath('//table[@id="historyTable_{}"]/tr/td[4]/a/text()'.format(table_num)) # KB 핫픽스 버전 ID 추출
    return release

def new_release():
    r = requests.get("https://winrelinfo.blob.core.windows.net/winrelinfo/ko-KR.html")
    parser = html.fromstring(r.content)
    release = []
    cnt = 0
    for p in parser.getiterator('h4'):
        cnt +=1
        release.append(parser.xpath('//*[@id="winrelinfo_container"]/h4[{}]/a/text()'.format(cnt))[1].strip())

    return release

def wiki_os_version(url,tr):
    r = requests.get(url)
    parser = html.fromstring(r.content)
    release = parser.xpath('//table[@class="infobox vevent"]/tr[{}]/td[1]/text()'.format(tr))
    if "5.1.2600.5512" in release:
        # Windows XP
        release = re.search(re.compile("(.*)( 서비스)"), release[0]).group(1)
    elif "6.1.7601" in release:
        # Windows 7 / Windows Server 2008 R2
        release = re.search(re.compile("(\()(.*)(\))"),release[0]).group(2)
    elif "6.0.6002" in release:
        # Windows Server 2008
        release = re.search(re.compile("(.*)(\()"),release[0]).group(1)
    elif "5.2.3790.3959" in release:
        # Windows Server 2003
        release = re.search(re.compile("(.*)( 서비스)"),release[0]).group(1)
    elif "5.0.3700.6690" in release:
        # Windows 2000
        release = re.search(re.compile("(v2 \()(.*)(\))"),release[0]).group(2)

    return release

def servicePack(os_version,release):
    try:
        pack = "OS 버전 : " + str(os_version) + "\n" + "최신 빌드는 : [Build " + str(release) + "] 입니다."
    except:
        pack = "OS 버전 : " + str(os_version) + "\n" + "최신 빌드는 : [Build " + str(release) + "] 입니다."
    return pack

def check_ServicePack():
    os_version = platform.system() +" "+ platform.version()
    os_service_ver = platform.version()
    service_ver = new_release()
    release = None
    try:
        os_service_ver = re.search(re.compile(".*(?<=\.)([0-9]+)"),os_service_ver).group(1)
    except AttributeError:
        result = "귀하의 버전은 현재 프로그램에 등재되어 있지 않은 신규 버전 혹은 에러일수 있습니다."
        return result
    if "10" in platform.release():
        flag = False
        for number in range(len(service_ver)):
            if os_service_ver in service_ver[number]:
                release = ms_os_version(number)
                flag = True
                break
        if flag is False:
            result = "귀하의 버전은 현재 프로그램에 등재되어 있지 않은 신규 버전 혹은 에러일수 있습니다."
            return result
        result = ServicePack_10_2016(release,os_version)

    elif "XP" in platform.release():
        release = wiki_os_version("https://ko.wikipedia.org/wiki/%EC%9C%88%EB%8F%84%EC%9A%B0_XP#.EC.97.AD.EC.82.AC",6)
        result = ServicePack_XP(os_service_ver,release,os_version)

    elif "2012" in platform.release():
        # 2012 | 2012 R2
        release = wiki_os_version("https://ko.wikipedia.org/wiki/%EC%9C%88%EB%8F%84%EC%9A%B0_%EC%84%9C%EB%B2%84_2012#.EC.9C.88.EB.8F.84.EC.9A.B0_.EC.84.9C.EB.B2.84_2012_R2",6)
        result = ServicePack_Window2012_R2(os_service_ver,release,os_version)

    elif "2008" in platform.release():
        if "R2" in platform.release():
            release = wiki_os_version("https://en.wikipedia.org/wiki/Windows_7", 8)
            result = ServicePack_Window2008_R2(os_service_ver,release,os_version)
        else:
            # 그냥 2008
            release = wiki_os_version("https://ko.wikipedia.org/wiki/%EC%9C%88%EB%8F%84%EC%9A%B0_%EC%84%9C%EB%B2%84_2008",6)
            result = ServicePack_Window2008_R2(os_service_ver,release,os_version)
    elif "2003" in platform.release():
        release = wiki_os_version("https://ko.wikipedia.org/wiki/%EC%9C%88%EB%8F%84%EC%9A%B0_%EC%84%9C%EB%B2%84_2003",7)
        result = ServicePack_Window2003(os_service_ver,release,os_version)

    elif "2000" in platform.release():
        release = wiki_os_version("https://ko.wikipedia.org/wiki/%EC%9C%88%EB%8F%84%EC%9A%B0_2000",7)
        result = ServicePack_Window2000(os_service_ver,release,os_version)

    elif "7" in platform.release():
        release = wiki_os_version("https://en.wikipedia.org/wiki/Windows_7",8)
        result = ServicePack_7(os_service_ver,release,os_version)

    return result

# 완
def ServicePack_10_2016(release,os_version):
    try:
        result = None
        status = None
        get_hotfix = os.popen("chcp 437 | wmic qfe get hotfixid")
        gethotfix = get_hotfix.read().replace("KB","KB ").strip()
        get_hotfix.close()
        flag = False
        cnt = 0
        for r in range(len(release)):
            cnt = r
            if release[cnt] in gethotfix:
                pack = "현재 사용중인 OS 버전은 최신 Service Pack 입니다."
                result = servicePack(os_version, release[cnt]) + "\n" + pack
                status = "양호"
                flag = True
                break
        if flag is False:
            pack = "현재 사용중인 OS 버전은 최신 Service Pack이 아닙니다."
            result = servicePack(os_version, release[cnt]) + "\n" + pack
            status = "취약"
    except:
        result = "Error 설치된 MS HotFix가 존재하지 않거나 에러가 발생하였습니다."
        status = "비 정상"
    return result,status

# 완
def ServicePack_7(os_service_ver,release,os_version):
    result = None
    status = None
    if "6.1.7601" in os_service_ver:
        if os_service_ver in release:
            pack = "현재 사용중인 OS 버전은 최신 Service Pack 입니다."
            result = servicePack(os_version, release) + "\n" + pack
            status = "양호"
    else:
        pack = "현재 사용중인 OS 버전은 최신 Service Pack이 아닙니다."
        result = servicePack(os_version, release) + "\n" + pack
        status = "취약"
    return result,status

# 완
def ServicePack_XP(os_service_ver,release,os_version):
    result = None
    status = None
    if "5.1.2600" in os_service_ver:
        if os_service_ver in release:
            pack = "현재 사용중인 OS 버전은 최신 Service Pack 입니다."
            result = servicePack(os_version, release) + "\n" + pack
            status = "양호"
    else:
        pack = "현재 사용중인 OS 버전은 최신 Service Pack이 아닙니다."
        result = servicePack(os_version, release) + "\n" + pack
        status = "취약"
    return result,status

# 완 2012 / 2012 R2
def ServicePack_Window2012_R2(os_service_ver,release,os_version):
    result = None
    status = None
    if "6.3.9600" in os_service_ver:
        if os_service_ver in release:
            pack = "현재 사용중인 OS 버전은 최신 Service Pack 입니다."
            result = servicePack(os_version, release) + "\n" + pack
            status = "양호"
        else:
            pack = "현재 사용중인 OS 버전은 최신 Service Pack이 아닙니다."
            result = servicePack(os_version, release) + "\n" + pack
            status = "취약"
        return result,status

# 완
def ServicePack_Window2008_R2(os_service_ver,release,os_version):
    result = None
    status = None
    if "6.1.7601" in os_service_ver:
        if os_service_ver in release:
            pack = "현재 사용중인 OS 버전은 최신 Service Pack 입니다."
            result = servicePack(os_version, release) + "\n" + pack
            status = "양호"
    else:
        pack = "현재 사용중인 OS 버전은 최신 Service Pack이 아닙니다."
        result = servicePack(os_version, release) + "\n" + pack
        status = "취약"
    return result,status
    # Windows Server 2012 / 2012 R2

# 완
def ServicePack_Window2008(os_service_ver,release,os_version):
    result = None
    status = None
    if "6.0.6002" in os_service_ver:
        if os_service_ver in release:
            pack = "현재 사용중인 OS 버전은 최신 Service Pack 입니다."
            result = servicePack(os_version, release) + "\n" + pack
            status = "양호"
    else:
        pack = "현재 사용중인 OS 버전은 최신 Service Pack이 아닙니다."
        result = servicePack(os_version, release) + "\n" + pack
        status = "취약"
    return result,status

# 완
def ServicePack_Window2003(os_service_ver,release,os_version):
    result = None
    status = None
    if "5.2.3790" in os_service_ver:
        if os_service_ver in release:
            pack = "현재 사용중인 OS 버전은 최신 Service Pack 입니다."
            result = servicePack(os_version, release) + "\n" + pack
            status = "양호"
    else:
        pack = "현재 사용중인 OS 버전은 최신 Service Pack이 아닙니다."
        result = servicePack(os_version, release) + "\n" + pack
        status = "취약"
    return result,status

# 완
def ServicePack_Window2000(os_service_ver,release,os_version):
    result = None
    status = None
    if "5.0.2195" in os_service_ver:
        if os_service_ver in release:
            pack = "현재 사용중인 OS 버전은 최신 Service Pack 입니다."
            result = servicePack(os_version, release) + "\n" + pack
            status = "양호"
    else:
        pack = "현재 사용중인 OS 버전은 최신 Service Pack이 아닙니다."
        result = servicePack(os_version, release) + "\n" + pack
        status = "취약"
    return result,status

if __name__ == '__main__':
    check_ServicePack()