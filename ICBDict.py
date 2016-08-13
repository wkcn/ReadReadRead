#-*- coding:utf-8 -*-

import urllib2
import xml.dom.minidom

def GetHTML(word):
    url = "http://dict-co.iciba.com/api/dictionary.php?w=%s&key=40AAB9CEFD02DA381C2DCB7A512BCB0F" % word
    req = urllib2.Request(url)
    resp = urllib2.urlopen(req)
    data = resp.read()
    return data

def ICBDict(word):
    data = GetHTML(word)
    dom = xml.dom.minidom.parseString(data)
    res = {
            "ps":[],
            "voice":[],
            "trans":[],
            "ex":[]
        }
    pos = dom.getElementsByTagName("pos")
    acceptation = dom.getElementsByTagName("acceptation")
    for i in range(len(acceptation)):
        p = ""
        a = "" 
        if pos[i].firstChild != None:
            p = pos[i].firstChild.data[:-1]
        if acceptation[i].firstChild != None:
            a = acceptation[i].firstChild.data[:-1]
        res["trans"].append((p, a))
    orig = dom.getElementsByTagName("orig")
    trans = dom.getElementsByTagName("trans")
    for i in range(len(orig)):
        res["ex"].append((orig[i].firstChild.data[:-1], trans[i].firstChild.data[:-1]))

    pron = dom.getElementsByTagName("pron")
    ps = dom.getElementsByTagName("ps")
    for i in range(len(pron)):
        res["voice"].append(pron[i].firstChild.data)
    for i in range(len(ps)):
        res["ps"].append(ps[i].firstChild.data)
    if len(ps) == 0:
        res["ps"] = ['','']
    return res
