from fastapi import FastAPI
import requests
from selenium import webdriver
from config import config

app = FastAPI()

mode = config('config.ini', 'Display')['mode']

if mode == 'common':
    driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
elif mode == 'extend':
    driver_in = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
    driver_out = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
else:
    print("Error")

@app.get('/display')
def display_extend(type: str = None, id: str = None, gate: str = None):
    try:
        url = config('config.ini', 'Webserver')['url']
        url = '{0}?type={1}&rfid={2}&Gate={3}'.format(url, type, id, gate)
        print('Requesting to url:', url )
        if mode == 'extend':
            if type == 'IN':
                driver_in.get(url)
                return {"result": "complete"}
            elif type == 'OUT':
                driver_out.get(url)
                return {"result": "complete"}
            else:
                return {"result": "fail"}
        elif mode == 'common':
            driver.get(url)
            return {"result": "complete"}
    except:
            return {"result": "fail"}

