
import binascii as ubinascii
import json as ujson 
import requests as urequests
import time as utime
     
Key = 'Insert Key Here'

def GetFunFact():
     urlBase = 'http://catfact.ninja'
     urlValue = urlBase + "/fact"
     try:
          value = urequests.get(urlValue).text
          data = ujson.loads(value)
          #print(data)
          result = data.get("fact")
     except Exception as e:
          print(e)
          result = 'failed'
     return result

def SL_setup():
     urlBase = "https://api.systemlinkcloud.com/nitag/v2/tags/"
     headers = {"Accept":"application/json","x-ni-api-key":Key}
     return urlBase, headers
     
def Put_SL(Tag, Type, Value):
     urlBase, headers = SL_setup()
     urlValue = urlBase + Tag + "/values/current"
     propValue = {"value":{"type":Type,"value":Value}}
     try:
          reply = urequests.put(urlValue,headers=headers,json=propValue).text
     except Exception as e:
          print(e)         
          reply = 'failed'
     return reply

def Get_SL(Tag):
     urlBase, headers = SL_setup()
     urlValue = urlBase + Tag + "/values/current"
     try:
          value = urequests.get(urlValue,headers=headers).text
          data = ujson.loads(value)
          #print(data)
          result = data.get("value").get("value")
     except Exception as e:
          print(e)
          result = 'failed'
     return result     

while True:
    wantcat = Get_SL('catbool')
    wantcatbool = True if wantcat == 'true' else False
    print(wantcatbool)

    if wantcatbool == True:
        funfact = GetFunFact()
        print(funfact)
        Put_SL('catfact','STRING',funfact)
        utime.sleep(4)
