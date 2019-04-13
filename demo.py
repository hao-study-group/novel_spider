import requests

headers = {
    "Range": "bytes=0-10485760",
    "Vpwp-Type": "preloader",
    "Vpwp-Key": "F444287966D15BF3A54421620F222362",
    "Vpwp-Raw-Key": "v0200f870000biltof9q4do8dp6krbfg_h265_540p_473722",
    "Vpwp-Flag": "0",
    "Accept-Encoding": "identity",
    "Host": "v6-dy.ixigua.com",
    "Connection": "Keep-Alive",
    "User-Agent": "okhttp/3.10.0.1",

}

url = 'http://oth.eve.mdt.qq.com:8080/analytics/upload?rid=1211eb90fa4cdea2&sid=a7984f3815f65b04e09d4853ae233373'
# res = requests.get(url=url,headers=headers)
# with open('xx.mp4','wb') as f:
#     f.write(res.content)

import pymysql


