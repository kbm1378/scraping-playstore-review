# !/usr/bin/python
# -*- coding: utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import xlsxwriter
from pandas import Series, DataFrame
import pandas as pd
from pandas import ExcelWriter

#import sys
#import importlib
#importlib.reload(sys)
#sys.setdefaultencoding('utf-8')


driver = webdriver.Chrome('/Users/byungmook/Documents/dev/crawler/chromedriver')
driver.implicitly_wait(3)

#id = 'com.time.is.gold' #시간은금이다
#id = 'com.leum.eon' #블루레몬
#id = 'com.cashslide' #캐시슬라이드
#id = 'com.cashwalk.cashwalk' #캐시워크
#id = 'kr.co.mediaweb.picacoin.admaster' #피카코인
#id = 'com.ssg.bang' #방치타임
id = 'com.photocard.master' #포토카드 마스터앱
driver.get('https://play.google.com/store/apps/details?id='+ id + '&hl=ko')
#driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

dt_result = DataFrame()

for i in range(0, 100):
    for j in range(0, 15):
        try:
            driver.find_element_by_xpath('//*[@id="body-content"]/div/div/div[1]/div[2]/div[2]/div[1]/div[4]/button[2]/div[2]/div/div').click()
            time.sleep(0.2)
            #element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="body-content"]/div/div/div[1]/div[2]/div[2]/div[1]/div[4]/button[2]/div[2]/div/div')))
        except:
            continue

    html = driver.page_source # 페이지의 elements모두 가져오기
    soup = BeautifulSoup(html, 'html.parser') # BeautifulSoup사용하기
    reviews = soup.find_all("div", attrs={"class": "single-review"})
    print(i)


    dt_result = DataFrame()

    for review in reviews:
        star =  review.find("div", attrs={"class": "tiny-star"}).get('aria-label').replace("별표 5개 만점에 ","").replace("개로 평가했습니다.","")
        review_text =  review.find("div", attrs={"class":"review-body"}).text.replace("전체 리뷰","")
        result = [star, review_text]
        dt_result = dt_result.append([result])

    dt_result.to_excel('play_store_review_' + id + '.xlsx', sheet_name='Sheet1', engine='xlsxwriter')
