# -*- coding: utf-8 -*-
__author__ = "Chirag Rathod (Srce Cde)"
__license__ = "GPL 3.0"
__email__ = "chiragr83@gmail.com"
__maintainer__ = "Chirag Rathod (Srce Cde)"

import requests
import pandas as pd


def openURL(URL, params):
    r = requests.get(URL + "?", params=params)
    return r.text


def create_df(df_payload, save_path):
    df = pd.DataFrame().from_dict(df_payload)
    df.to_csv(save_path)
