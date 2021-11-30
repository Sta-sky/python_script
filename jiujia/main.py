import requests
import urllib3.contrib.pyopenssl
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 解决告警
urllib3.contrib.pyopenssl.inject_into_urllib3()
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

"""
解决SSL问题
pip install cryptography
pip install pyOpenSSL
pip install certifi
"""


def get_info():
    headers = {
        "Host": "cloud.cn2030.com",
        "Connection": "keep-alive",
        "Cookie": "ASP.NET_SessionId=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MzgyNjE4MjguMDU4ODk0NCwiZXhwIjoxNjM4MjY1NDI4LjA1ODg5NDQsInN1YiI6IllOVy5WSVAiLCJqdGkiOiIyMDIxMTEzMDA0NDM0OCIsInZhbCI6IkFBQUFBQUlBQUFBUU5qbGhNakF3TkRGaE1qUTFPV1JqTlJ4dmNYSTFielZCVmxSaFkzRmtZVzUxYm1sNmRscGxkV3N4YmtSTkFCeHZcclxuVlRJMldIUTNVRGRzWldGeVVsQkZiemRNZDBsVVgyaFdOREJCRGpFM01TNHlNVE11TlRrdU1UZzJBQUFBQUFBQUFBPT0ifQ.KpmQ7suEZTjr39GcFhuHO_zh_KQTPg727G79L8hagPU",
        "User-Agent": "Mozilla/5.0(WindowsNT6.1;WOW64) AppleWebKit/537.36(KHTML,likeGecko)Chrome/53.0.2785.143Safari/537.36MicroMessenger/7.0.9.501NetType/WIFIMiniProgramEnv/WindowsWindowsWechat",
        "content-type": "application/json",
        "zftsl": "c8086100843bb232e246319cbc4cf3c6",
        "Referer": "https://servicewechat.com/wx2c7f0f3c30d99445/91/page-frame.html",
        "Accept-Encoding": "gzip, deflate, br"
    }


    url = 'https://cloud.cn2030.com/sc/wx/HandlerSubscribe.ashx?act=CustomerList&city=%5B%22%22%2C%22%22%2C%22%22%5D&lat=30.57447&lng=103.92377&id=0&cityCode=0&product=1'
    print(url)
    res = requests.get(url, headers=headers, verify=False).text
    print(res)


if __name__ == '__main__':
    print('开始运行')
    get_info()

