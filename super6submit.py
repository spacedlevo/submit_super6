#!/usr/bin/env python

from bs4 import BeautifulSoup
import requests

login_site = 'https://www.skybet.com/secure/identity/m/login/super6'
play_page = 'https://super6.skysports.com/play'
super6_pundits_url = 'https://super6.skysports.com/pundits'


# THESE SHOULD REALLY NOT BE HARDCODED INTO SCRIPT. TRY USING ENVIRO VARIABLES
# OR HOLD IN A SEPERATE FILE
user = '#ADD USER'
pwd = '#ADD PASSWORD'
pushover_keys = {}


def create_scores(predictions):
    data = {}
    r = s.get(play_page)
    soup = BeautifulSoup(r.content, 'html.parser')
    match_cards = soup.find_all('div', class_='js-challenge flex-item prediction-card prediction-card__prelive')
    ids = [card['data-challenge-id'] for card in match_cards]
    for id_ in ids:
        fixtures = soup.find_all('div', {'data-challenge-id':id_})
        for fixture in fixtures:
            teams = [i['data-shortname'] for i in fixture.find_all('p', class_='team-name flush--bottom js-team-name')]
            for num, team in enumerate(teams, 1):
                data["score[{}][team{}]".format(id_, num)] = predictions[team]
                data["score[{}][team{}]".format(id_, num)] = predictions[team]
    data["confirmed"] = 1
    data["goldengoal[{}]".format(int(ids[-1]) + 1)] = 11
    data["_csrf_token"] = soup.find('input', {'name':'_csrf_token'})['value']
    submit = s.post(play_page, data=data, timeout=3)
    return submit.status_code

def super6_login():
    paras = {'username': user, 'pin': pwd}
    headers =  {    
                'Host':'www.skybet.com',
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0',
                'Accept': 'application/json',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Referer': 'https://www.skybet.com/secure/identity/m/login/super6?urlconsumer=https://super6.skysports.com&dl=1',
                'content-type': 'application/json',
                'x-requested-with': 'XMLHttpRequest',
                'Origin': 'https://www.skybet.com',
                'Content-Length': '38',
                'Connection': 'keep-alive'
    }
    token_json = s.post(login_site, json=paras, headers=headers)
    user_token = token_json.json()['user_data']['ssoToken']
    s.post('https://super6.skysports.com/auth/login', data={'token':user_token})
    return None

def pushover_notification(body):        
    params = {'token':pushover_keys['token'], 'user':pushover_keys['user'], 'message':body}
    requests.post('https://api.pushover.net/1/messages.json', params=params)
    return None

with requests.Session() as s:
    prediction_dict = {}
    if len(prediction_dict) > 1:
        super6_login()
        create_scores(prediction_dict)
        pushover_notification("Super6 Done")
    else:
        print("No Predictions Yet!")
