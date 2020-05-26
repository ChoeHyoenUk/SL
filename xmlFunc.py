from xml.etree import ElementTree
import http.client
from xml.dom.minidom import parseString
import urllib.request

key = '23534542e0be066999d2803d1057fc37'
conn = http.client.HTTPSConnection("www.kobis.or.kr")


def DailyRanking(period):
    params = '?key=' + key + '&targetDt=' + period
    conn.request('GET', '/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.xml' + params)
    res = conn.getresponse()
    if int(res.status) == 200:
        strXml = parseString(res.read().decode('utf-8')).toprettyxml()

        tree = ElementTree.fromstring(strXml)
        items = list(tree.iter("dailyBoxOffice"))
        for item in items:
            name = item.find('movieNm')
            ranking = item.find('rank')
            sales = item.find('salesAcc')
            audi = item.find('audiAcc')
            print("영화 제목: " + name.text)
            print("박스오피스 순위: " + ranking.text)
            print("누적 매출: " + sales.text)
            print("누적 관객: " + audi.text)
            print()
    else:
        print("HTTP Request is failed :" + res.reason)
        print(res.read().decode('utf-8'))


def WeaklyRanking(period):
    params = '?key=' + key + '&targetDt=' + period + '&weekGb=0'
    conn.request('GET', '/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.xml' + params)
    res = conn.getresponse()
    if int(res.status) == 200:
        strXml = parseString(res.read().decode('utf-8')).toprettyxml()
        tree = ElementTree.fromstring(strXml)
        items = list(tree.iter("weeklyBoxOffice"))
        for item in items:
            name = item.find('movieNm')
            ranking = item.find('rank')
            sales = item.find('salesAcc')
            audi = item.find('audiAcc')
            print("영화 제목: " + name.text)
            print("박스오피스 순위: " + ranking.text)
            print("누적 매출: " + sales.text)
            print("누적 관객: " + audi.text)
            print()
    else:
        print("HTTP Request is failed :" + res.reason)
        print(res.read().decode('utf-8'))
