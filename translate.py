# -*- coding: utf-8 -*-
#
# Time-stamp: <Wednesday 2020-06-24 14:34:20 AEST Graham Williams>
#
# Copyright (c) Togaware Pty Ltd. All rights reserved.
# Licensed under the MIT License.
# Author: Graham.Williams@togaware.com
# 
# https://github.com/MicrosoftTranslator/Text-Translation-API-V3-Python


"""A mlhub command line interface to Azure Translate.

Useage: ml translate aztranslate --to=fr [--path=<path>] [<sentence>]
"""

# ----------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------

DEFAULT_TO_LANGUAGE = "en"

# Import the required libraries.

import os
import sys
import json
import argparse
import requests

from mlhub.pkg import azkey, is_url
from mlhub.utils import get_cmd_cwd

# ----------------------------------------------------------------------
# Parse command line arguments
# ----------------------------------------------------------------------

option_parser = argparse.ArgumentParser(add_help=False)

option_parser.add_argument(
    'sentence',
    nargs="*",
    help='text to translate')

option_parser.add_argument(
    '--path', '-p',
    help='path to a text file')

option_parser.add_argument(
    '--to', "-t",
    help=f'destination language ({DEFAULT_TO_LANGUAGE})')

args = option_parser.parse_args()

if args.to is None: args.to = DEFAULT_TO_LANGUAGE

if args.path and args.sentence:
    option_parser.error("either a path OR sentence allowed but not both.")

# ----------------------------------------------------------------------
# Request subscription key and location from user.
# ----------------------------------------------------------------------

SERVICE   = "Translator"
KEY_FILE  = os.path.join(os.getcwd(), "private.txt")

key, location = azkey(KEY_FILE, SERVICE, connect="location", verbose=False)

headers  = {
    'Ocp-Apim-Subscription-Key': key,
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json',
}  

endpoint      = 'https://api.cognitive.microsofttranslator.com/'
path          = '/translate?api-version=3.0'
translate_url = endpoint + path

# ----------------------------------------------------------------------
# Read the text to be translated.
# ----------------------------------------------------------------------

#print("sentence =>", args.sentence)
#print("path =>", args.path)
# print("to =>", args.to)
# print()
text = ""
if args.path:
    text = open(os.path.join(get_cmd_cwd(), args.path), "r").read()
elif args.sentence:
    text = " ".join(args.sentence)
# print("text =>", text)
# print()

# ----------------------------------------------------------------------
# Support function to translate the text.
# ----------------------------------------------------------------------

def translate(text, to):
    json   = [{'text': text}]
    params = f'&to={to}'
    result = requests.post(translate_url + params, headers=headers, json=json)
    result = result.json()

    sys.stdout.write(f"{result[0]['detectedLanguage']['language']}," +
                     f"{result[0]['detectedLanguage']['score']}," +
                     f"{result[0]['translations'][0]['to']}," +
                     f"{result[0]['translations'][0]['text']}")
    sys.stdout.flush()

# ----------------------------------------------------------------------
# Translate the text.
# ----------------------------------------------------------------------

if len(text):
    translate(text, args.to)
    print()
else:
    if sys.stdin.isatty():
        try:
            for line in sys.stdin:
                translate(line, args.to)
        except KeyboardInterrupt:
            pass
    else:
        for line in sys.stdin.readlines():
            translate(line, args.to)
