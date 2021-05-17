import os
from mlhub.pkg import get_private


# ----------------------------------------------------------------------
# Request subscription key and endpoint from user.
# ----------------------------------------------------------------------

def request_priv_info():
    PRIVATE_FILE = "private.json"

    path = os.path.join(os.getcwd(), PRIVATE_FILE)

    private_dic = get_private(path, "aztranslate")

    subscription_key = private_dic["Translator"]["key"]

    endpoint = private_dic["Translator"]["location"]
    return subscription_key, endpoint
