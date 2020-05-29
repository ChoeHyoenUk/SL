from xml.etree import ElementTree
import requests

kobisKey = '23534542e0be066999d2803d1057fc37'
kmdbKey = 'N1UG972286869QC55WOA'


def DailyRanking(period):
    url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.xml'
    params = '?key=' + kobisKey + '&targetDt=' + period
    url += params
    res = requests.get(url).text
    tree = ElementTree.fromstring(res)
    return tree


def WeaklyRanking(period):
    url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.xml'
    params = '?key=' + kobisKey + '&targetDt=' + period
    url += params
    res = requests.get(url).text
    tree = ElementTree.fromstring(res)
    return tree


def GetPosterURL(title, releaseDts):
    url = 'http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_xml2.jsp?collection=kmdb_new2'
    url += '&ServiceKey=' + kmdbKey + '&title=' + title + '&releaseDts=' + releaseDts
    res = requests.get(url).text
    tree = ElementTree.fromstring(res)
    items = tree.iter('Row')
    for item in items:
        releaseDate = item.find('ratings').find('rating').find('releaseDate').text.replace(' ', '')
        if releaseDate == releaseDts:
            posterURL = item.find('posters').text.split('|')[0].replace(' ', '')
            if posterURL == '':
                return 'NoImage'
            else:
                return posterURL
    return 'NoImage'
