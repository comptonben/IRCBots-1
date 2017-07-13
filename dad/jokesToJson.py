#!/usr/bin/python

import json
from pprint import pprint

def convertTextFile():
    data = None
    with open('config.json') as json_file, open('dadJokes.txt') as text_file:
        data = json.load(json_file)
        for line in text_file:
            data['speak']['dadName']['responses']['joke'].append([line.split('~')[0] + "\n" + line.split('~')[1].replace("\n", "")])
    rewriteJsonFile(data)

def addJoke(joke):
    data = None
    with open('config.json') as json_file:
        data = json.load(json_file)
        data['speak']['dadName']['responses']['joke'].append([joke])
    rewriteJsonFile(data)

def rewriteJsonFile(data):
    with open('config.json', 'w') as json_file:
        json.dump(data, json_file, sort_keys=True, indent=4)

if __name__ == "__main__":
    main()