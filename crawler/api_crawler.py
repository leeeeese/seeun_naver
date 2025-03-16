import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import urllib.request
import json
import re
import time
import os
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By

# .env 파일 로드
load_dotenv()

# 네이버 검색/블로그/플레이스 크롤러(api)


class NaverCrawler:
    def __init__(self):
        # API 키를 .env 파일에서 로드
        self.API_keys = []
        for i in range(1, 9):
            client_id = os.getenv(f'NAVER_CLIENT_ID_{i}')
            client_secret = os.getenv(f'NAVER_CLIENT_SECRET_{i}')
            if client_id and client_secret:
                self.API_keys.append({
                    "client_id": client_id,
                    "client_secret": client_secret
                })

        self.HEADERS = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}

    def HELP(self):
        print("[get_BlogURL]:input=query,num\n  -query:검색어\n  -num:크롤링 할 글 수 결정\n  >>output:[url1, url2, ...]\n")
        print(
            "[get_BlogInfo]:input=url,image\n  -url:블로그 링크\n  -image:TRUE/FALSE,이미지까지 크롤링할지 결정\n  >>output:\"안녕하세요. 오늘은 ...\", [img1, img2, ...]\n")
        print(
            "[get_NaverPlace]:input=location,name\n  -location:장소 위치\n  -name:장소명\n  >>output:[category, tel_num, review, extra_inform]")

    def get_numTxt(self, query):
        Search = urllib.parse.quote(query)

        # json 결과
        url = f"https://openapi.naver.com/v1/search/blog?query={Search}"

        for API in self.API_keys:
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id", API["client_id"])
            request.add_header("X-Naver-Client-Secret", API["client_secret"])
            try:
                response = urllib.request.urlopen(request)
                rescode = response.getcode()
            except:
                continue
            blog_url = []
            if (rescode == 200):
                response_body = response.read()
                msg = response_body.decode('utf-8')
                tot_num = json.loads(msg)['total']
                break
            else:
                continue

        return tot_num

    def get_BlogURL(self, query, num):
        # 블로그 url 가져오기
        keyword = []
        Search = urllib.parse.quote(query)

        start = 1
        size = num
        # json 결과
        url = f"https://openapi.naver.com/v1/search/blog?query={Search}&start={start}&display={size}"

        for API in self.API_keys:
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id", API["client_id"])
            request.add_header("X-Naver-Client-Secret", API["client_secret"])
            try:
                response = urllib.request.urlopen(request)
                rescode = response.getcode()
            except:
                continue
            blog_url = []
            if (rescode == 200):
                response_body = response.read()
                msg = response_body.decode('utf-8')
                blog = json.loads(msg)['items']
                tot_num = json.loads(msg)['total']
                for blog_info in blog:
                    for word in keyword:
                        if (word in blog_info['title'].split(" ")):
                            continue
                    blog_url.append(blog_info['link'])
                break
            else:
                continue

        return blog_url, tot_num

    def get_BlogInfo(self, url, img=False):
        # 블로그 정보 가져오기
        cont = ''
        imgs = []
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            ifra = soup.find('iframe', id='mainFrame')
            post_url = 'https://blog.naver.com' + ifra['src']
            res = requests.get(post_url)
            soup2 = BeautifulSoup(res.text, 'html.parser')

            txt_contents = soup2.find_all(
                'div', {'class': "se-module se-module-text"})

            for p_span in txt_contents:
                for txt in p_span.find_all('span'):
                    cont += txt.get_text()
                if (img == True):
                    imgs = soup2.find_all('img', class_='se-image-resource')
        except:
            pass
        return cont, imgs

    def get_NaverPlace(self, location, name):
        url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=" + \
            f"{quote(location)}+{quote(name)}"
        res = requests.get(url, headers=self.HEADERS)
        soup = BeautifulSoup(res.text, "lxml")
        naver_place = soup.find_all(
            "div", attrs={"class": "api_subject_bx"})[0]

        # 카테고리 가져오기
        category = naver_place.find(
            "span", attrs={"class": "DJJvD"}).get_text()
        # 전화번호 가져오기
        try:
            tel = naver_place.find("li", attrs={"class": "SF_Mq SjF5j Xprhw"})
            tel_num = tel.find("span", attrs={"class": "dry01"}).get_text()
        except:
            tel_num = None
        # 방문자 리뷰 가져오기
        try:
            rev = naver_place.find("ul", attrs={"class": "flicking-camera"})
            reviews = rev.find_all("li", attrs={"class": "nbD78"})
            # num_review = len(reviews)
            txt = []
            for review in reviews:
                txt.append(review.find("span", attrs={
                           "class": "nWiXa"}).get_text()[1:-2])
        except:
            txt.append(None)
        # 기타 부가 정보
        try:
            extra = naver_place.find("div", attrs={"class": "xHaT3"})
            etc = extra.find("span", attrs={"class": "zPfVt"}).get_text()
        except:
            etc = None

        inform = [category, tel_num, txt, etc]
        return inform
