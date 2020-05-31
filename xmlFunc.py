from xml.etree import ElementTree
import requests
import urllib

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


def GetPosterURL_openDt(title, releaseDts):
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


def GetPosterURL_actor(title, actor):
    url = 'http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_xml2.jsp?collection=kmdb_new2'
    url += '&ServiceKey=' + kmdbKey + '&title=' + title + '&actor=' + actor
    res = requests.get(url).text
    tree = ElementTree.fromstring(res)
    items = tree.iter('Row')
    for item in items:
        posterURL = item.find('posters').text.split('|')[0].replace(' ', '')
        if posterURL == '':
            return 'NoImage'
        else:
            return posterURL
    return "NoImage"


def GetActorAndDirector(name):
    url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.xml'
    url += '?key=' + kobisKey + '&peopleNm=' + name + '&itemPerPage=100'
    res = requests.get(url).text
    tree = ElementTree.fromstring(res)
    items = tree.iter('people')
    l = []
    for item in items:
        role = item.find('repRoleNm').text
        if role == '감독' or role == '배우':
            peopleName = item.find('peopleNm').text
            peopleCode = item.find('peopleCd').text
            l.append((peopleName, peopleCode))
    return l


def GetFilmo(code):
    url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleInfo.xml'
    url += '?key=' + kobisKey + '&peopleCd=' + code
    res = requests.get(url).text
    tree = ElementTree.fromstring(res)
    items = tree.iter('filmo')
    l = []
    for item in items:
        movieNm = item.find('movieNm').text
        movieCd = item.find('movieCd').text
        l.append((movieNm, movieCd))
    return l


def GetDetailInfo(code):
    url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.xml'
    url += '?key=' + kobisKey + '&movieCd=' + code
    res = requests.get(url).text
    tree = ElementTree.fromstring(res)
    infoTree = tree.iter('movieInfo')
    for info in infoTree:
        movieNm = '제목: ' + info.find('movieNm').text
        runtime = '상영 시간: ' + info.find('showTm').text
        openDt = '개봉일: ' + info.find('openDt').text

        genreTree = info.iter('genre')
        genre = '장르: '
        for g in genreTree:
            genre += g.find('genreNm').text

        directorTree = info.iter('director')
        director = '감독: '
        for d in directorTree:
            director += d.find('peopleNm').text

        actorTree = list(info.iter('actor'))
        actor = '출연 배우: '
        for i in range(3):
            actor += actorTree[i].find('peopleNm').text + ' '

        auditTree = info.iter('audit')
        watchGradeNm = '관람 등급: '
        for w in auditTree:
            watchGradeNm += w.find('watchGradeNm').text

        DetailInfoStr = movieNm + '\n' + \
                        runtime + '\n' + \
                        openDt + '\n' + \
                        genre + '\n' + \
                        director + '\n' + \
                        actor + '\n' + \
                        watchGradeNm

    return DetailInfoStr
