# -*- coding: utf-8 -*-
#
# Time-stamp: <Tuesday 2020-06-23 17:08:06 AEST Graham Williams>
#
# Copyright (c) TogawarePty Ltd. All rights reserved.
# Licensed under the MIT License.
# Author: Graham.Williams@togaware.com
#
# This demo is based on the Azure Cognitive Services Translator Quick Starts
# 
# https://github.com/MicrosoftTranslator/Text-Translation-API-V3-Python
#

from mlhub.pkg import mlask, mlcat
from mlhub.utils import get_private

mlcat("Limitations of Translations", """\
Douglas Hofstadter, a professor of cognitive science and comparative
literature at Indiana University at Bloomington and author of the book
Gödel, Escher, Bach, highlights in a January 2018 article in The
Atlantic the limitations of automated language translation. To
paraphrase, the translators do not have any deep understanding of the
text but have developed a shallower mechanical process to do a decent job
for simple communications.

Below we illustrate the issue with one of Hofstadter's examples. See the
original article for details:

https://www.theatlantic.com/technology/archive/2018/01/the-shallowness-of-google-translate/551570/

The original article demonstrated the issue using Google Translator. We
demonstrate using Azure Translator.
""")

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

hof_or = [{'text': """In their house, everything comes in pairs. There's his car
and her car, his towels and her towels, and his library and hers."""}]

mlcat("Sample Text", hof_or[0]['text'])

params   = '&to=fr'
request = requests.post(translate_url + params, headers=headers, json=hof_or)
hof_fr = request.json()

mlask(begin="\n", end="\n")

mlcat("French Translation", hof_fr[0]['translations'][0]['text'])

mlask(begin="\n", end="\n")

# ----------------------------------------------------------------------

mlcat("Translating Back to English", """\
Translating bask to English demonstrates the shallow understanding
of the actual text. The machine learning model does not really 
understand the text and through the understanding is able to translate 
accurately. In fact, the model has a superficial understanding which
results in some mis-understanding.
""")

params   = '&to=en'
request = requests.post(translate_url + params,
                        headers=headers,
                        json=hof_fr[0]['translations'])
hof_en = request.json()

mlask(end="\n")

sys.stdout.write(fill(hof_en[0]['translations'][0]['text']))

mlask(begin="\n\n", end="\n")

# ----------------------------------------------------------------------

mlcat("Compare to Google Translator", """\
Dans leur maison, tout vient en paires. Il y a sa voiture et sa
voiture, ses serviettes et ses serviettes, sa bibliothèque et
les siennes.

Then

At home, they have everything in double. There is his own car
and his own car, his own towels and his own towels, his own
library and his own library.
""")
