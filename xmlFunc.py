from xml.etree import ElementTree
import requests
import urllib

kobisKey = '23534542e0be066999d2803d1057fc37'
kmdbKey = 'N1UG972286869QC55WOA'
theater_key = '7d0f32ab2f3d4c949ce02fb87a89332a'


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
    if releaseDts is None:
        return 'NoImage'
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


def GetPosterURL_director(title, director):
    url = 'http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_xml2.jsp?collection=kmdb_new2'
    url += '&ServiceKey=' + kmdbKey + '&title=' + title + '&director=' + director
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


def GetActor(name):
    url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.xml'
    url += '?key=' + kobisKey + '&peopleNm=' + name + '&itemPerPage=100'
    res = requests.get(url).text
    tree = ElementTree.fromstring(res)
    items = tree.iter('people')
    l = []
    for item in items:
        role = item.find('repRoleNm').text
        if role == '배우':
            peopleName = item.find('peopleNm').text
            peopleCode = item.find('peopleCd').text
            l.append((peopleName, peopleCode))
    return l


def GetDirector(name):
    url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.xml'
    url += '?key=' + kobisKey + '&peopleNm=' + name + '&itemPerPage=100'
    res = requests.get(url).text
    tree = ElementTree.fromstring(res)
    items = tree.iter('people')
    l = []
    for item in items:
        role = item.find('repRoleNm').text
        if role == '감독':
            peopleName = item.find('peopleNm').text
            peopleCode = item.find('peopleCd').text
            l.append((peopleName, peopleCode))
    return l


def GetMovies(name):
    movieNm_utf8 = urllib.parse.quote(name)
    url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.xml'
    url += '?key=' + kobisKey + '&movieNm=' + movieNm_utf8 + '&itemPerPage=100'
    res = requests.get(url).text
    tree = ElementTree.fromstring(res)
    items = tree.iter('movie')
    l = []
    for item in items:
        movieNm = item.find('movieNm').text
        movieCd = item.find('movieCd').text
        openDt = item.find('openDt').text
        l.append((movieNm, movieCd, openDt))
    return l


def GetFilmo(code, element):
    if element == '배우':
        url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleInfo.xml'
        url += '?key=' + kobisKey + '&peopleCd=' + code
        res = requests.get(url).text
        tree = ElementTree.fromstring(res)
        items = tree.iter('filmo')
        l = []
        for item in items:
            if item.find('moviePartNm').text == '배우':
                movieNm = item.find('movieNm').text
                movieCd = item.find('movieCd').text
                l.append((movieNm, movieCd))
        return l

    elif element == '감독':
        url = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleInfo.xml'
        url += '?key=' + kobisKey + '&peopleCd=' + code
        res = requests.get(url).text
        tree = ElementTree.fromstring(res)
        items = tree.iter('filmo')
        l = []
        for item in items:
            if item.find('moviePartNm').text == '감독':
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
        if not info.find('movieNm').text is None:
            movieNm = '제목: ' + info.find('movieNm').text
        else:
            movieNm = '제목: '

        if not info.find('showTm').text is None:
            runtime = '상영 시간: ' + info.find('showTm').text
        else:
            runtime = '상영 시간: '

        if not info.find('openDt').text is None:
            openDt = '개봉일: ' + info.find('openDt').text
        else:
            openDt = '개봉일: '

        genreTree = info.iter('genre')
        genre = '장르: '
        for g in genreTree:
            genre += g.find('genreNm').text + ' '

        directorTree = info.iter('director')
        director = '감독: '
        for d in directorTree:
            director += d.find('peopleNm').text + ' '

        actorTree = list(info.iter('actor'))
        actor = '출연 배우: '
        actorCount = 0
        for actors in actorTree:
            actor += actors.find('peopleNm').text + ' '
            actorCount += 1
            if actorCount == 3:
                break

        auditTree = info.iter('audit')
        watchGradeNm = '관람 등급: '
        for w in auditTree:
            if not w.find('watchGradeNm').text is None:
                watchGradeNm += w.find('watchGradeNm').text
                break

        DetailInfoStr = movieNm + '\n' + \
                        runtime + '\n' + \
                        openDt + '\n' + \
                        genre + '\n' + \
                        director + '\n' + \
                        actor + '\n' + \
                        watchGradeNm

    return DetailInfoStr


def GetLocation(name):
    Location_utf8 = urllib.parse.quote(name)
    url = 'https://openapi.gg.go.kr/MovieTheater'
    url += '?key=' + theater_key + '&SIGUN_NM=' + Location_utf8
    res = requests.get(url).text
    tree = ElementTree.fromstring(res)
    items = tree.iter('row')
    l = []
    cnt = 0
    for item in items:
        BIZPLC_NM = item.find('BIZPLC_NM').text
        REFINE_WGS84_LOGT = item.find('REFINE_WGS84_LOGT').text  # 경도
        REFINE_WGS84_LAT = item.find('REFINE_WGS84_LAT').text  # 위도
        BSN_STATE_NM = item.find('BSN_STATE_NM').text  # 영업상태
        REFINE_ZIP_CD = item.find('REFINE_ZIP_CD').text  # 우편번호
        REFINE_LOTNO_ADDR = item.find('REFINE_LOTNO_ADDR').text  # 도로명주소
        cnt1 = 0
        for i in BIZPLC_NM:
            if i == "제":
                BIZPLC_NM = BIZPLC_NM.replace("제", "")
            elif i == "관":
                BIZPLC_NM = BIZPLC_NM.replace("관", "")
        # 숫자 제거
        new_BIZPLC_NM = ''.join([i for i in BIZPLC_NM if not i.isdigit()])
        if (BSN_STATE_NM == "영업중"):
            if cnt == 0:
                l.append(((new_BIZPLC_NM, REFINE_WGS84_LOGT, REFINE_WGS84_LAT, REFINE_ZIP_CD, REFINE_LOTNO_ADDR)))
                cnt += 1
            for i in l:
                if i[3] != REFINE_ZIP_CD:
                    cnt1 += 1
            if (cnt1 == len(l)):
                l.append(((new_BIZPLC_NM, REFINE_WGS84_LOGT, REFINE_WGS84_LAT, REFINE_ZIP_CD, REFINE_LOTNO_ADDR)))
    return l
