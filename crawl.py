import requests

baseUrl = "https://www.aqistudy.cn/"

def crawl_factor(postfix, headers, data=None):
    url = baseUrl + postfix
    try:
        response = requests.get(url, headers=headers) if data is None else requests.post(url, headers=headers, data=data)
        return response.text
    except Exception as e:
        print(e)
        return None

    