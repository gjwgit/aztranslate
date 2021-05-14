# -*- coding: utf-8 -*-
#
# Time-stamp: <Tuesday 2020-06-23 17:07:41 AEST Graham Williams>
#
# Copyright (c) Togaware Pty Ltd. All rights reserved.
# Licensed under the MIT License.
# Author: Graham.Williams@togaware.com
#
# Command line tool to list supported languages.
#
# ml languages aztranslate
# 
# https://github.com/MicrosoftTranslator/Text-Translation-API-V3-Python
#

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------

# Import the required libraries.

import os
import sys
import json
import requests

from mlhub.utils import get_private

# ----------------------------------------------------------------------
# Request subscription key and location from user.
# ----------------------------------------------------------------------

PRIVATE_FILE = "private.json"

path = os.path.join(os.getcwd(), PRIVATE_FILE)

private_dic = get_private(path, "aztranslate")

key = private_dic["Translator"]["key"]

location = private_dic["Translator"]["location"]

headers  = {
    'Ocp-Apim-Subscription-Key': key,
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json',
}  

endpoint      = 'https://api.cognitive.microsofttranslator.com/'
path          = '/languages?api-version=3.0'
languages_url = endpoint + path

response = requests.get(languages_url, headers=headers)
response = response.json()
translations = response['translation']

for l in translations:
    t = translations[l]
    print(f"{l},{t['dir']},{t['name']},{t['nativeName']}")
