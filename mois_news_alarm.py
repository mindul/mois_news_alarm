# coding: utf-8
# 행정안전부 보도자료를 텔레그램으로 보내기
# 개발언어 : Python 3
# 버전 :  1.0
# 작성일 : 2019. 9. 15.

import requests
import urllib
import urllib3
from bs4 import BeautifulSoup
from urllib.request import urlopen
import time

urllib3.disable_warnings()
http = urllib3.PoolManager()

url = "https://www.mois.go.kr/frt/bbs/type010/commonSelectBoardList.do?bbsId=BBSMSTR_000000000008"

# telegram url(change your bot API token)
Teleg_URL = "https://api.telegram.org/bot230190712:AGHTKGdIVC134_8Gi1GYUsvHx87BlpOeyS3/sendMessage?chat_id=65796221&text="
DOMAIN = '\nhttps://www.mois.go.kr'

filename = 'LatestNoMois.txt'

# 2차원 배열(box) 선언과 초기화
box = [['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','',''],['','','']]

# 가장 최신 게시물 번호를 파일에 저장하기
def PutTheLatestNo():

    params = {
        "nttId": 0,
        "bbsTyCode": "BBST03",
        "bbsAttrbCode": "BBSA03",
        "authFlag": "Y",
        "pageIndex": "1",
        "cal_url": "/sym/cal/EgovNormalCalPopup.do",
        "searchCnd": 0,
    }

    response = requests.post(url, params)
    dom = BeautifulSoup(response.content, "html.parser")
    elements = dom.select(".table_style1.mobile > tbody > tr")

    LastNo = elements[0].select_one("td").text.strip()

    output_file = open(filename, 'w')
    output_file.write(LastNo)


# 파일에 저장된 게시물 번호 가져오기
def GetTheNoFromFile():
    input_file = open(filename, 'r')
    fileNo = input_file.readline()
    input_file.close()
    return(fileNo)


# 텔레그램으로 알람 보내기
def SendMessage( strTitle, article_URL ):
    target_URL = DOMAIN + article_URL
    strTelMsg = '{}{}{}{}'.format( Teleg_URL, urllib.parse.quote("[행정안전부 보도자료]\n "), urllib.parse.quote(strTitle), urllib.parse.quote(target_URL))

    http.request('GET', strTelMsg).data


# 메인 함수
def news_table():

    params = {
        "nttId": 0,
        "bbsTyCode": "BBST03",
        "bbsAttrbCode": "BBSA03",
        "authFlag": "Y",
        "pageIndex": "1",
        "cal_url": "/sym/cal/EgovNormalCalPopup.do",
        "searchCnd": 0,
    }

    response = requests.post(url, params)
    dom = BeautifulSoup(response.content, "html.parser")
    elements = dom.select(".table_style1.mobile > tbody > tr")

    # 파일에 저장된 번호 읽어오기
    NoFromFile = GetTheNoFromFile()

    i = 0

    for element in elements:

        box[i][0] = element.select_one("td").text.strip()
        box[i][1] = element.select_one("a").text
        box[i][2] = element.select_one("a").get("href")

        i = i + 1

    # 최신 게시물이라면 텔레그램으로 메시지 발송
    for j in range(0, 10):   # 0~9
        if int(box[j][0]) > int(NoFromFile):  # 최신 게시물인지 비교
            SendMessage(box[j][1], box[j][2]) # 제목, URL 발사!

while True:
    # 메인 함수 실행
    news_table()

    # 가장 최신 게시물 번호를 파일에 저장
    PutTheLatestNo()

    time.sleep(60*60*1)   # every 1hour