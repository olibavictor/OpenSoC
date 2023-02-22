#!/usr/bin/env python3
#By Oliba

import requests
import json
from datetime import datetime, timezone, timedelta

def GetToken():
        tenantId = '55c016b2-c932-4ce4-8cfe-992e3903e553'
        clientId = 'b1bb3cb5-bef2-479f-a38b-8eb6432cb6e6'
        clientSecret = 'LDH8Q~~EwB6FG4oKSJ-CacqYWBvmS4R9-HxvBaty'
        resourceAPI = 'https://graph.microsoft.com'
        url = "https://login.microsoftonline.com/" + tenantId + "/oauth2/token"
        data = {
                'resource' : resourceAPI,
                'client_id' : clientId,
                'client_secret' : clientSecret,
                'grant_type' : 'client_credentials'
        }
        reqpost = requests.post(url, data)
        token_data = reqpost.json()
        auth_token = token_data['access_token']
        return auth_token

def GetAlert(auth_token, createdDateTime):
        url = "https://graph.microsoft.com/v1.0/security/alerts?$filter=vendorInformation/provider eq 'Office 365 Security and C                                       ompliance' or vendorInformation/provider eq 'MCAS' and createdDateTime gt " + createdDateTime + "&$top=1"
        headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'Authorization': "Bearer " + auth_token
        }
        reqget = requests.get(url, headers=headers)
        alert_json = reqget.json()['value']
        json_string = json.dumps(alert_json)
        return json_string

def GetUTCtime():
        currentTimeDate = datetime.now(timezone.utc) - timedelta(minutes=1)
        currentTime = currentTimeDate.isoformat()[:-9]+'Z'
        return currentTime

alertvalue = GetAlert(GetToken(), GetUTCtime())
if alertvalue == "[]":
        exit()
else:
        alert = '{"value": ' + alertvalue + '}'
        print(alert)
