# -*- coding:utf-8 -*-
import os
import sys
import http.client
from xml.dom.minidom import parseString
import urllib.request

client_id = "84863q160e"
client_secret = "oqZ6c0ZjHpzuX62dK9TKNAVVLRV4hfVlNfqkgPvq"

#conn = http.client.HTTPConnection("naveropenapi.apigw.ntruss.com/map-static")
#headers = {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret}



def GetMap(x,y):
    center = x + "," + y
    level = "16"
    width = "550"
    url = "https://naveropenapi.apigw.ntruss.com/map-static/v2/raster"
    height = "550"
    format = "png8"
    parmas = "?w="+ width +"&h="+ height +"&center="+center+"&level="+level+"&format="+format+"&dataversion=201.3"
    url += parmas
    resp = None

    req = urllib.request.Request(url)
    req.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
    req.add_header("X-NCP-APIGW-API-KEY", client_secret)

    try:
        resp = urllib.request.urlopen(req)
    except urllib.error.URLError as e:
        print(e.reason)
        print(parseString(e.read().decode('utf-8')).toprettyxml())
    except urllib.error.HTTPError as e:
        print("error code=" + e.code)
        print(parseString(e.read().decode('utf-8')).toprettyxml())
    else:
        response_body = resp.read()
        return response_body


    #conn.request("GET", "/v2/raster" + parmas, None, headers)
    #res = conn.getresponse()



#GetMap("127.1054221","37.3591614")