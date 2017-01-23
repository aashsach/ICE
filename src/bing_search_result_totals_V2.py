#!/usr/bin/Python3.5
# --coding:utf-8--

import os
import unicodedata, re, os
from bs4 import BeautifulSoup
from .bing_search_api import BingSearchAPI
from random import randint, sample
from urllib.request import quote

def bing_search_total(_verbose, _search_phrase, _bing_api_key):

    def cache_abs_path(cache_rel_path):
        script_dir = os.path.dirname(__file__)
        return os.path.join(script_dir, cache_rel_path)

    

    #_search_phrase_parsed = "%22" + _search_phrase.replace(' ', '+').strip(' ') + "%22" # %22 acts as quotes, facilitating a phrase search
    _search_phrase_parsed = "%22" + quote(_search_phrase.strip(' ')) + "%22"
    _bing_parameters = {'$format': 'json', '$top': 2}

    #Set up a cache to remember the total number of hit searches retried
    with open(cache_abs_path("cache/bing_search_totals.cache"), 'r') as f:
        diction = {}
        print(_search_phrase_parsed)
        for line in f:
            phrase, hit = line.split('/----/')
            try:
                hit = ''.join(filter(lambda x: x.isdigit(), hit))
                diction[phrase] = int(hit)
            except Exception as e:
                print("Diction cache error for " + hit)

    with open(cache_abs_path("cache/bing_search_totals.cache"), 'a') as f:
        if _search_phrase in diction:
            return diction[_search_phrase], _bing_api_key
        else:
            count = 0
            while True:
                count = count + 1
                try:
                    _bing_search = BingSearchAPI(_bing_api_key)
                    res = _bing_search.search('web', _search_phrase_parsed, _bing_parameters).json()
                    total_search_results = res["d"]["results"][0]["WebTotal"]
                    print('-----' + str(total_search_results) + '-----------')
                    total = int(total_search_results)
                    if(isinstance(total, int)):
                        if _verbose:
                            print('\t', _search_phrase_parsed.replace('+', ' ').replace('%22', ''), total)
                            pass
                        print("%s/----/%d" % (_search_phrase, total), file = f)
                        return total, _bing_api_key
                except Exception as e:
                    if _verbose:
                        print('\tERROR: in bing.search() - search total\n\t' + str(e))
                    print('\tERROR: in bing.search() - search total\n\t' + str(e))
                    print('\tEither network connection error or Bing Api key expired. Search phrase: ' + _search_phrase_parsed)
                    if count < 10:
                        with open(cache_abs_path("cache/Bing_API_keys.cache")) as keys_file:
                            keys = list()
                            for line in keys_file:
                                keys.append(line)
                            _bing_api_key = ''.join(filter(lambda x: (ord(x) < 128), sample(keys, 1)[0].strip(' \t\n\r')))
                    else:
                        _bing_api_key = input("Please enter another Bing API key: ")
                        count = 0

            
# Test
#bing_search_total(True, "Natural Language Processing", "U5Px9AJDGqcMOJVfwZLFa5GfCHi1e6DLwCl+0tt/NX4")
