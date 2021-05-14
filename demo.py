# -*- coding: utf-8 -*-
#
# Time-stamp: <Tuesday 2020-07-07 16:26:05 AEST Graham Williams>
#
# Copyright (c) Togaware Pty Ltd. All rights reserved.
# Licensed under the MIT License.
# Author: Graham.Williams@togaware.com
#
# This demo is based on the Azure Cognitive Services Translator Quick Starts
# 
# https://github.com/MicrosoftTranslator/Text-Translation-API-V3-Python
#

from mlhub.pkg import mlask, mlcat
from mlhub.utils import get_private

mlcat("Azure Text Translation", """\
Welcome to a demo of the pre-built models for Text Translation provided
through Azure's Cognitive Services. This service translates text between
multiple languages.
""")

mlask()
# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------

# Import the required libraries.

import os
import sys
import json
import requests

from textwrap import fill

# ----------------------------------------------------------------------
# Request subscription key and location from user.
# ----------------------------------------------------------------------

PRIVATE_FILE = "private.json"

path = os.path.join(os.getcwd(), PRIVATE_FILE)

private_dic = get_private(path, "aztranslate")

key = private_dic["Translator"]["key"]

location = private_dic["Translator"]["location"]

# ----------------------------------------------------------------------
# Prepare to send requests to the service.
# ----------------------------------------------------------------------

headers  = {
    'Ocp-Apim-Subscription-Key': key,
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json',
}  

endpoint      = 'https://api.cognitive.microsofttranslator.com/'
path          = '/translate?api-version=3.0'
translate_url = endpoint + path

endpoint      = 'https://api.cognitive.microsofttranslator.com/'
path          = '/languages?api-version=3.0'
languages_url = endpoint + path

# ----------------------------------------------------------------------

mlcat("Supported Languages", """\
These are the languages supported by the Azure Translator for translation.
""")

response = requests.get(languages_url, headers=headers)
response = response.json()
translations = response['translation']

count = 1 # For lines per page.
for l in translations:
    if count%20 == 0:
        mlask(True, True)
    t = translations[l]
    print(f"{l:8} {t['dir']} {t['name']:25} {t['nativeName']:25}")
    count += 1

mlcat("", f"""\
That's {count} languages in total.
""", begin="\n")

mlask(True)

# ----------------------------------------------------------------------

mlcat("Text Translation from English", """\
Below we demonstrate the translation of a variety of common phrases as we might
find when interacting with a voice command system.""")

utterances = [{ 'text': """\
    Hi Tom, has my parcel arrived yet?
    Where is a good shop to buy mobile phones?
    Has Frederick replied to my email yet?
    We are running late, please start without us.
    Tell me the most important message this morning?
    When is a good time to meet Susan and Dave?
"""}]

print("\n" + utterances[0]['text'])
    
params   = '&to=de&to=it&to=fr&to=id&to=hi&to=ar&to=th&to=zh-Hant'
request = requests.post(translate_url + params, headers=headers, json=utterances)
response = request.json()

lang  = response[0]['detectedLanguage']
trans = response[0]['translations']

mlcat("", f"""\
The supplied text was detected as '{lang['language']}' with a 
score of '{lang['score']}'.""")

for t in trans:
    mlask(True, True,
          f"Press Enter for a translation to {translations[t['to']]['name']}")
    sys.stdout.write(t['text'])

mlask(True, True, "Press Enter to continue on to translations back to English")

# ----------------------------------------------------------------------

mlcat("Translation back to English", """\
Below we translate each of the above translations back to English. Again the 
source language is automatically identified.

Here's a reminder of the original English utterances:
""")

print(utterances[0]['text'][:-1]) # Remove final \n.

params   = '&to=en'
request = requests.post(translate_url + params, headers=headers, json=trans)
reverse = request.json()

for t in reverse:
    lang  = t['detectedLanguage']
    trans = t['translations']
    mlask(True, True,
          f"Press Enter for the translation from " +
          f"{translations[lang['language']]['name']} " +
          f"(language id score={lang['score']})")
    sys.stdout.write(trans[0]['text'])

print()
