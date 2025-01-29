import urllib
import requests
import urllib
import pandas as pd
import json
import time
import datetime
import threading
from dataIO import *

baseUrl = "https://air.cnemc.cn:18007/CityData/GetAQIDataPublishLive"
def crawl(cityName):
    url = baseUrl +"?cityName="+ urllib.parse.quote(cityName+"市")
    try:
        response = requests.get(url)
        return response.text
    except Exception as e:
        print(e)
        return None
    

def extract_data_to_dataframe(json_string):
    try:
        data = json.loads(json_string)

        if data:
            df = pd.DataFrame(data)
            return df
        else:
            return None

    except json.JSONDecodeError:
      print("Error: Invalid JSON format.")
      return None
    except Exception as e:
      print(f"An error occurred: {e}")
      return None

def run_at_the_hour(func, *args, **kwargs):
    def run_job():
        while True:
            now = datetime.datetime.now()
            next_hour = now.replace(minute=0, second=0, microsecond=0) + datetime.timedelta(hours=1)
            wait_seconds = (next_hour - now).total_seconds()
            time.sleep(wait_seconds)
            
            try:
                func(*args, **kwargs)
            except Exception as e:
                 print(f"Error executing function {func.__name__}: {e}")
    
    thread = threading.Thread(target=run_job, daemon=True)
    thread.start()
    
def crawl_perHour(message):
    now = datetime.datetime.now()
    print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] Message: {message}")
    cities = read_from_txt('cities.txt')
    for city in cities:
        data_json = crawl(city)
        df = extract_data_to_dataframe(data_json)
        print(df)


if __name__ == "__main__":
    # 在每个整点执行 example_function 函数，传递一个消息作为参数
    run_at_the_hour(crawl_perHour, message="Executing crawl_perHour...")

    # 让主线程保持运行，以便后台线程可以继续执行
    try:
      while True:
        time.sleep(1) # 主线程休眠 1 秒，防止CPU占用过高
    except KeyboardInterrupt:
        print("Exiting...")