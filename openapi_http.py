# -*- coding:utf-8 -*-
import os
import sys
import http.client
from xml.dom.minidom import parseString
import urllib.request

client_id = "84863q160e"
client_secret = "oqZ6c0ZjHpzuX62dK9TKNAVVLRV4hfVlNfqkgPvq"
Accept = "application/xml"


def GetMap(x,y):
    center = x + "," + y

    level = "16"
    width = "550"
    url = "https://naveropenapi.apigw.ntruss.com/map-static/v2/raster"
    height = "550"
    format = "png8"
    parmas = "?w="+ width +"&h="+ height +"&markers=type:d|size:tiny|pos:"+x+"%20"+y+"&format="+format+"&dataversion=201.3"
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


def subDetailMap(start,goal):
    startP = start
    goalP = goal
    url = "https://naveropenapi.apigw.ntruss.com/map-direction-15/v1/driving"


def getXY(Address):
    query = Address
    url = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"
    parmas = "?query="+query
    url += parmas

    resp = None

    req = urllib.request.Request(url)
    req.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
    req.add_header("X-NCP-APIGW-API-KEY", client_secret)
    req.add_header("Accept", Accept)
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
        print(parseString(response_body.decode('utf-8')).toprettyxml())
        return response_body

