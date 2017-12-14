import re
import requests
import os
from lxml import html
from fake_useragent import UserAgent
ua = UserAgent()

ms_headers = {
    'Accept':'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
	'Content-Type': 'text/html; charset=utf-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Connection': 'Keep-Alive',
    'Cookie':'ak_bmsc=16049D1D5AF3328EE800EB60C44F980E1723DA4F2C580000B050025A2B1B8F1E~plrzChhaL92PA13x2j/83L108F1s056zUC1YiODX46BHSFpMfX/62L6CrHbpE/ke4jdjEt0+Jj/K1ETtw7a1G9m7MJ3MSZyxA1GMBbCRZXVRn3H5reb2GuhMguotw+DCvPfpLYueDMwKRazpTEyy+iTUpr5mOECUfmPW50LOs1S8RTMrQQVapvxSuO55MYPSf1vwLqhW1IXsg2bwrIJWdRJlzuw4Mph8tAkp2LrDH8dI4=; MS-CV=QKUalLMTVEXhoehqwNM3Mx.0; MC1=GUID=f5d857c1296841e89d0dae21c8967eac&HASH=f5d8&LV=201711&V=4&LU=1510101168709; MSFPC=ID=7fd1b9a55aebb64cb117559099336812&CS=1&LV=201711&V=1; MSFPC=GUID=f5d857c1296841e89d0dae21c8967eac&HASH=f5d8&LV=201711&V=4&LU=1510101168709; A=I&I=AxUFAAAAAAAtBgAAQnFjchRBK2sxdKSz9S9SbA!!&V=4; MUID=0713AAAD81696E2D3CD0A19985696D17; ASP.NET_SessionId=lsvnztzkxdbosfl4fk4bgs4c; gssLANG=ko; optimizelyEndUserId=oeu1510103479070r0.46162046322055095; MC0=1510103478798; graceIncr=0; smcexpsessionticket=100; smcpartner=smc; WRUIDAWS=1475064137416242; __CT_Data=gpv=14&ckp=tld&dm=microsoft.com&apv_1020_www32=15&cpv_1020_www32=15&rpv_1020_www32=15; MS0=c668907518bf43bbbfa557fca34616f3; smc_f=premiervolta-1|mlc-1|dad-1|pslc-1|aad-1|mnb-1|vm-1|cqpm-1|cantilever-1|hiva-1|hucsu-1|sfe-1|sds-1|spc-1|smc-survey-feat-1|smc-survey-elg-0|vafx-usvc-1|dbscp-1|sri-1|eu-cookie-banner-1|smc-cat-nav-1|sc-2|legie-1|modapicomp-1|smc-clicktale-0|dsf-1|ustrl-1|surface-hub-1|asicsoverride-1|vafx-blob-1|hoops-tz-1|smc-ci-4; smc_ci=4; smc_t=2017-11-08T02:10:18.7207591Z; SMCsiteLang=en-IE; SMCsiteDir=ltr; smcflighting=100; bm_sv=F2F4F67456FFED43FB0A46359C62EBDA~l6U2YbrDgFmtfHCEkUk3Zrmyqa8RcXO3KP8AMjIxfEIBhcUGAV25ZZ5T0bf5iqNQqLlnskftbwZe6zzmGw80VQK5ZI3vfy8SP1anMz1ODiVAN9+QKAf2u4iHu0I3bNkedn+E0XW0tWmEJHWSM38n1EDpdh83l+zSQH+1j/c52ig='
}
url = "https://support.microsoft.com/en-ie/help/4018124/windows-10-update-history"
url2 = "https://support.microsoft.com/ko-kr/help/4000825/windows-10-windows-server-2016-update-history"
r = requests.post(url=url,headers=ms_headers)
a = r.json()