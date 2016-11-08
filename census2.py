#!/usr/bin/env python

import urllib.request
import ast
import simplejson as json
import requests
from pprint import pprint
from util import state_code_map


with open('../secrets.json') as f:    
    secrets = json.load(f)

class City(object):
    def __init__(self, place_id, state_code, year=2010, dataset='sf1'):
        self.key = secrets['census_api_key']
        self.place_id = place_id
        self.state_id = state_code_map[state_code]
        self.year = year
        self.dataset = dataset
        self.labels = ['name', 'population',  'housing_units', 'housing_occupied', 'housing_vacant'] + ['state_id', 'city_id', 'race_white', 'race_black', 'race_native', 'race_asian', 'race_pacisland', 'race_other', 'race_mixed']
        self.fields = ['NAME', 'P0010001', 'H0030001', 'H0030002', 'H0030003', 'P0030002', 'P0030003', 'P0030004','P0030005','P0030006','P0030007','P0030008',]

    def info(self):
        url = 'http://api.census.gov/data/{}/{}'.format(self.year, self.dataset)

        payload = {'key': self.key}

        payload['get'] = [','.join(self.fields)]
        payload['for'] = 'place:{}'.format(self.place_id)
        payload['in'] = 'state:{}'.format(self.state_id)


        r = requests.get(url, params=payload)
        json = r.json()

        return dict(zip(self.labels, json[1]))


class State(object):
    def __init__(self, state_code, year=2010, dataset='sf1'):
        self.key = apikey
        self.state_id = state_code_map[state_code]
        self.year = year
        self.dataset = dataset
        self.fields = ['NAME', 'P0010001']
        self.labels = ['name', 'population'] + ['state_id', ]

    def info(self):
        url = 'http://api.census.gov/data/{}/{}'.format(self.year, self.dataset)

        payload = {'key': self.key}

        payload['get'] = [','.join(self.fields)]
        payload['for'] = 'state:{}'.format(self.state_id)

        r = requests.get(url, params=payload)

        return dict(zip(self.labels, r.json()[1]))

    def cities(self):
        url = 'http://api.census.gov/data/{}/{}'.format(self.year, self.dataset)

        payload = {'key': self.key}
        payload['get'] = [','.join(self.fields)]
        payload['in'] = 'state:{}'.format(self.state_id)
        payload['for'] = 'place:*'

        r = requests.get(url, params=payload)

        labels = ['name', 'population', 'state_id', 'place_id', ]
        return [dict(zip(labels, x)) for x in r.json()]

    def counties(self):
        url = 'http://api.census.gov/data/{}/{}'.format(self.year, self.dataset)

        payload = {'key': self.key}
        payload['get'] = [','.join(self.fields)]
        payload['in'] = 'state:{}'.format(self.state_id)
        payload['for'] = 'county:*'

        r = requests.get(url, params=payload)

        labels = ['name', 'population', 'state_id', 'county_id', ]
        return [dict(zip(labels, x)) for x in r.json()]

c = State('CA')
info = c.info()
pprint(info)
counties = c.counties()
pprint(counties)
cities = c.cities()
pprint(cities)


city = City('43000', 'CA')
city_info = city.info()
pprint(city_info)
