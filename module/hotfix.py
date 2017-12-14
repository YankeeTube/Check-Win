import re
import requests
import os
import platform
from lxml import html


def check_hotfix(url):
    r = requests.get(url)
    hotfix = r.json()
    hotfix = hotfix["links"][0]['articleId']  # 최신 핫픽스
    os_fix = os.popen("wmic qfe get hotfixid")  # OS의 설치된 Hotfix 추출
    if hotfix in os_fix:
        release = "[" + hotfix + "] 업데이트 완료"
    else:
        release = "[" + hotfix + "] 업데이트 누락"
    return release

def ms_os_version(table_num):
    r = requests.get("https://winrelinfo.blob.core.windows.net/winrelinfo/ko-KR.html")
    parser = html.fromstring(r.content)
    release = parser.xpath('//table[@id="historyTable_{}"]/tr/td[4]/a/text()'.format(table_num)) # KB 핫픽스 버전 ID 추출
    os_fix = os.popen("wmic qfe get hotfixid")  # OS의 설치된 Hotfix 추출
    if release[0] in os_fix:
        result = "[" + release[0] + "] 업데이트 완료"
    else:
        result = "[" + release[0] + "] 업데이트 누락"
    return result

def hotfix_comp():
    os_name = platform.release()
    if "7" or "2008" in os_name:
        result = check_hotfix("https://support.microsoft.com//app/content/api/content/asset/en-ie/4009472?iecbust=1496897351635")

    elif "2012" in os_name:
        result = check_hotfix("https://support.microsoft.com//app/content/api/content/asset/en-ie/4010478?iecbust=1496900716413")

    elif "8" or "8.1" or "2012 R2" or "2012 r2":
        result = check_hotfix("https://support.microsoft.com/app/content/api/content/asset/en-ie/4010477?iecbust=1496904350922")

    elif "2016" in os_name:
        result = ms_os_version(1)

    elif "10" in os_name:
        os_version = os.popen("chcp 437 | ver").read()
        os_service_ver = re.search(re.compile("(?<=)([0-9]+)(])"), os_version).group(1)  # 운영체제 버전에서 숫자 버전만 추출
        if "15063" in os_service_ver:
            result = ms_os_version(0)
        elif "14393" in os_service_ver:
            # windows 10 / Server 2016
            result = ms_os_version(1)
        elif "10586" in os_service_ver:
            result = ms_os_version(2)
        elif "10240" in os_service_ver:
            result = ms_os_version(3)

    elif "xp" or "XP" or "vista" or "VISTA" or "2000" or "NT" or "nt" or "2003":
        result = "해당 OS는 서비스가 종료되었습니다. OS 업그레이드를 권장합니다."

    else:
        result = "현재 프로그램에 적용되지 않은 모델입니다. 관리자에게 문의하십시오."

    return result

if __name__ == '__main__':
    print(ms_os_version(0))