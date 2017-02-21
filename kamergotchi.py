#!/usr/bin/python3
import requests
import time
import json
import dateutil.parser
import datetime
import random

xplayer = "player_id_here"
delayCheck = 60
delayConsumptionMin = 1
delayConsumptionMax = 3
readyForConsumption = False
baseUrl = "https://api.kamergotchi.nl/game";
reqHeaders = {'User-Agent': 'okhttp/3.4.1', 'x-player-token': xplayer, 'accept': 'application/json, text/plain, */*'}
reqHeadersPost = {'User-Agent': 'okhttp/3.4.1', 'x-player-token': xplayer, 'accept': 'application/json, text/plain, */*', 'Content-Type': 'application/json;charset=utf-8'}
consumptions = ['food', 'attention', 'knowledge']

def giveConsumption():
    typeNom = random.choice(consumptions)
    contentNom = '{"bar":"'+str(typeNom)+'"}'
    nomnomnom = requests.post(baseUrl+"/care", headers=reqHeadersPost, data=contentNom)
    nomStamp = datetime.datetime.now()
    print(str(nomStamp)+" Giving "+str(typeNom))
    try:
        jsonObj = nomnomnom.json()
    except ValueError:
        print("Received invalid JSON: "+str(nomnomnom.text()))
        return False
    if (jsonObj['game']['careLeft'] > 0):
        wachtFF = random.randint(delayConsumptionMin, delayConsumptionMax)
        time.sleep(wachtFF)
        giveConsumption()
    return True

def doClaim():
    claimStamp = datetime.datetime.now()
    print((claimStamp)+" Claiming!")
    claim = requests.post(baseUrl+"/claim", headers=reqHeaders)
    print(str(claim.json()))

def checkAPI():
    checkStamp = datetime.datetime.now()
    print(str(checkStamp)+" Checking with Kamergotchi API")
    check = requests.get(baseUrl, headers=reqHeaders)
    jsonObj = check.json()
    resetTime = dateutil.parser.parse(str(jsonObj['game']['careReset']))
    resetClaim = dateutil.parser.parse(str(jsonObj['game']['claimReset']))
    resetClaimTS = round(resetClaim.timestamp())
    resetTS = round(resetTime.timestamp()) 
    curTS = round(time.time())
    if (curTS - resetClaimTS > 0):
        doClaim()
    if (curTS - resetTS > 0):
        return True
    else:
        return False

def main():
    print("Norbie's Kamergotchi Bot v1.1")
    print("https://www.norbert.in/")
    print("-----------------------------")
    print("We're currently impersonating X-PLAYER "+xplayer)
    # Deze while loop kan veel eleganter:
    # checkAPI returned care/claim reset, in var stoppen en vergelijken ipv elke 60 sec te pollen.
    # Volgende versie jo!
    while True:
        while readyForConsumption == False:
            checkTrue = checkAPI()
            if checkTrue == True:
                break
            print("Not ready. Sleeping for "+str(delayCheck))
            time.sleep(delayCheck)
        giveConsumption()
        
if __name__ == "__main__":
    main()
