from urllib import response
import requests
import execjs
from urllib.parse import urlencode, quote
import urllib.request
from datetime import datetime
import time
import json
import io


json_result = {}
def extract_content(data, file):
    if isinstance(data, dict):
        # 如果是字典类型，则遍历字典中的每一个键值对
        for key, value in data.items():
            if isinstance(value, dict):
                # 如果值是字典类型，则递归调用extract_content函数
                extract_content(value, file)
            elif isinstance(value, list):
                for item in value:
                    extract_content(item, file)
            else:
                # Skip the DOUBLE which is the exemple sentences
                if (key != 'double') & (key != 'single'):
                    if key in ['dst', 'src', 'ph_en', 'ph_am', 'pos', 'word', 'tran', 'ex', 'def', 'text', 'enText', 'chText', 'word_mean']:
                        print('%s: %s' %(key, value))
                        file.write(f'{key}: {value}\n')
                        json_result[key] = value

    elif isinstance(data, list):
        # 如果是列表类型，则遍历列表中的每一个元素
        for item in data:
            extract_content(item, file)


def readJS(path):
    f = open(path, 'r')
    code = f.read()
    f.close()
    return code


def get_result(sign, trans, parame):

    base_url = 'https://fanyi.baidu.com/v2transapi?'
    fanyi_url = base_url + urlencode(parame)
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '137',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': 'APPGUIDE_10_0_2=1; REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; SOUND_PREFER_SWITCH=1; BIDUPSID=E0B35EC43FA41D972AE386409BA341F2; PSTM=1676274491; BAIDUID=D5CFE17DEA5C6723184945A3BA3A8859:FG=1; MCITY=-127%3A; BDUSS=d2M3lSYzFPMGNjdGlUdUJ1OHprQ2dDRlhMZXI4U3g3T204elZRUDFHOVdXVXBrRVFBQUFBJCQAAAAAAAAAAAEAAACS8Oj3cGFsYXRhYmtlAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFbMImRWzCJkRz; BDUSS_BFESS=d2M3lSYzFPMGNjdGlUdUJ1OHprQ2dDRlhMZXI4U3g3T204elZRUDFHOVdXVXBrRVFBQUFBJCQAAAAAAAAAAAEAAACS8Oj3cGFsYXRhYmtlAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFbMImRWzCJkRz; ZFY=g5Ev1ZZ:BpREfrsGCIKV36bQawLQErDHl3swnNkhwQIE:C; BAIDUID_BFESS=D5CFE17DEA5C6723184945A3BA3A8859:FG=1; __bid_n=1863a14f5da377d0954207; FPTOKEN=HDWbEe+vJFwBSoyQo7g93Q7IMZf8qAomcp5qmlJKkU6CZ/4FHYO3qbwEFUBp+2yBZapS95aplw0AKRuz8MGSmNc99z2UQNVIePKcm3R4paGzv2LVJTmTd0+2/DthoQsvoe4XdQiMRUKR+qa4skYLZH/gx/eoARbSK0VGIQdn2MvA2X+degINsy+ATMfHtloaSZ7Mr0qD4T4azkMRNFTJT8pr5ODSXLUNXbqjnnoB9+DGKxn2/BvHiTfGsZqZtL03hfQRqqw6Q/PZCFW++YrSkEQT+40hpP/hN+zvewGLjBt+8KfB3qhZ4cPKo8Ul4mHF4TiSz835mwP1RFfd4FbIOD0moVVELFB71MBLHPEvc+ezhtyBO28yYm5BaU0NnGDS+XcbPLhlWV52CoUdjo9z4Q==|+bNelxqDOpaZ0d8UK3clIU6RpL19O4kGGx5DAcbj3GQ=|10|57584cf8a4cc3b5899bed89a83dc3006; Hm_lvt_afd111fa62852d1f37001d1f980b6800=1686905352; Hm_lvt_64ecd82404c51e03dc91cb9e8c025574=1686828694,1686836999,1686881198,1686967853; Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574=1686967853; ab_sr=1.0.1_ZWVhNTMzYWRkZWI4OTQ0ZmJmNzNkZGU5MjczZjMyZjgxOGJhN2FjOTliYjExM2UyNWRkODQ2M2U2NGYxOWUwMDIwZjg3NDg2ODdmZjk1NzJkZTNmZGUzNTYwOWVhYTcxNjNkOTdkNTdhNmViODg2ODBmMmRjZWFmMWYwZmZiM2M0MmYyZmM4ODVmOWE5YTRmNWQzMDhmNmYyYjc1ZTU1MDFmMzRhNDlmMTMyMTlmMTYwZWI1ZTVmNjM4OGQzZjEx',
        'Host': 'fanyi.baidu.com',
        'Origin': 'https://fanyi.baidu.com',
        'Referer': 'https://fanyi.baidu.com/?aldtype=16047',
        'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43',
        'X-Requested-With': 'XMLHttpRequest',
    }

    ts = int(datetime.now().timestamp()*1000)
    data = {
        'from': parame['from'],
        'to': parame['to'],
        'query': trans,
        # 'transtype': 'enter',
        'transtype': 'realtime',
        'simple_means_flag': '3',
        'sign': sign,
        'token': 'Your token here',
        'domain': 'common',
        'ts': str(ts),
    }

    try:
        response = requests.post(fanyi_url, headers=headers, data=data)
        response =  response.json()
        outcome = response["trans_result"]['data'][0]['dst']
        response = json.dumps(response) 
        # print(response)
    except KeyError:
        return None, None
    return outcome, response


def get_sound_uk(from_text, to_text, lan):

    if lan == 'en':
        text = from_text
    else:
        text = to_text

    parame = {
        'lan': 'uk',
        'text': text,
        'spd': 3,
        'source': 'web'
    }
    sound_url = 'https://fanyi.baidu.com/gettts?' + urlencode(parame)
    sound_file = './sound_uk.mp3'
    urllib.request.urlretrieve(sound_url, sound_file)


def get_sound_us(from_text, to_text, lan):

    if lan == 'en':
        text = from_text
    else:
        text = to_text

    parame = {
        'lan': 'en',
        'text': text,
        'spd': 3,
        'source': 'web'
    }
    sound_url = 'https://fanyi.baidu.com/gettts?' + urlencode(parame)
    sound_file = './sound_us.mp3'
    urllib.request.urlretrieve(sound_url, sound_file)


class Translation:

    def __init__(self):
        self.__word = None
    
    def tran(self, word='hello'):

        # Do some preparation
        self.__word = word
        self.checkLan()
        parame = {
            'from': self.lan1,
            'to': self.lan2
        }
        ctx = execjs.compile(readJS(r'.\core\sign.js'))
        sign = ctx.call('e', self.__word)

        # Do the tranlation
        while(1):
            outcome, result = get_result(sign=sign, trans=self.__word, parame=parame)
            if outcome == None:
                print('Try again!')
                time.sleep(0.5)
                pass
            else:
                # print('result is ', result)
                history_book = io.open('.\\docs\\history.txt', 'r+', encoding='utf-8')
                history = history_book.read()

                now_query = io.open('.\\docs\\query.txt', 'w', encoding='utf-8')
                data = json.loads(result)
                extract_content(data, now_query)

                now_query = io.open('.\\docs\\query.txt', 'r', encoding='utf-8')
                now = now_query.read()
                history_book.seek(0, 0)
                history_book.write(now + '\n' + history)
                break
        
        # Get sounds
        get_sound_uk(self.__word, outcome, self.lan1)
        get_sound_us(self.__word, outcome, self.lan1)

        return outcome
        # return json_result 

    def checkLan(self):
        if '\u4e00' <= self.__word <= '\u9fff':
            self.lan1 = 'zh'
            self.lan2 = 'en'
        else:
            self.lan1 = 'en'
            self.lan2 = 'zh'


if __name__ == '__main__':
    w = input('请输入:')
    a = Translation()
    print(a.tran(w))
