from crawl import *
import execjs
import urllib
from decoder import *
from dataIO import *

def process_month_param(start, end):
    result = []
    while start <= end:
        result.append(str(start))
        if start % 100 == 12:
            start += 100
            start -= 11
        else:
            start += 1
    return result
            
def crawl_data(cityName, month):
    # obtain the key and iv from encrypted javascript file
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://www.aqistudy.cn"
    }
    js_file_encrypted = crawl_factor("/historydata/resource/js/de5CQkNmdaJwo.min.js?v=1695882361", headers=headers)
    js_file = eval_decoder(js_file_encrypted)
    decrypt_DES_key, decrypt_DES_iv, decrypt_AES_key, decrypt_AES_iv, encrypt_AES_key, encrypt_AES_iv,app_id = re_extractor_observe(js_file)
    

    # conmpile the javascript code and obtain the executable object ctx
    ctx = execjs.compile("const CryptoJS = require('crypto-js');\n" + js_file)

    # create the header of the request
    params = {
        "city": cityName,
        "month": month
    }
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Referer": "https://www.aqistudy.cn/historydata/daydata.php?city="+urllib.parse.quote(cityName)+"&month="+month,
        "Origin": "https://www.aqistudy.cn"
    }
    payload = {"hA4Nse2cT": headerCreator("GETDAYDATA", params, encrypt_AES_key, encrypt_AES_iv, app_id, ctx)}

    # obtain the encrypted data
    data_encrypted = crawl_factor("/historydata/api/historyapi.php", headers, data=payload)
    if data_encrypted == "":
        raise Exception("Failed to obtain the encrypted data of the city" + cityName)

    # decrypt the data
    data = data_decoder(data_encrypted, decrypt_DES_key, decrypt_DES_iv, decrypt_AES_key, decrypt_AES_iv, ctx)
    df = extract_data_to_dataframe(data)
    return df

if __name__ == '__main__':
    result = {}
    cities = read_from_txt('cities.txt')
    monthes = process_month_param(202312, 202312)
    for city in cities:
        for month in monthes:
            result[city + month] = crawl_data(cityName=city, month=month)
    print(result)