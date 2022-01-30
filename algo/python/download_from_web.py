# -*- coding: utf-8 -*-

# Download market volume history

import requests
import numpy as np
import logging
import sys

# https://www.codegrepper.com/code-examples/python/python+logging+to+file+and+console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)


def download_tickpilot_list():
    url = "http://tsp.finra.org/finra_org/ticksizepilot/TSPilotSecurities.txt"
    resp = requests.get(url)
    text = resp.content
    return text

def download_cboe_volume(Year=2020, monthly=False):
    url_tmpl = "https://www.cboe.com/us/equities/market_statistics/historical_market_volume/market_history_%s.csv-dl"
    if monthly:
        url_tmpl = "https://www.cboe.com/us/equities/market_statistics/historical_market_volume/market_history_monthly_%s.csv-dl"

    url = url_tmpl % str(Year)

    resp = requests.get(url)

    text = resp.content.decode('utf-8')
    return text


def download_cboe_volume_all_year():
    start_year = 2021
    nyear = 2 + (2021 - start_year)
    isMonthly = False

    for year in start_year + np.arange(nyear):
        res = download_cboe_volume(Year=year, monthly=isMonthly)
        filename = "c:/data/cboe/market_volume%s_%s.csv" % ("_monthly"
                        if isMonthly else "", str(year))
        logging.info("%s, count = %s, save to %s", year, len(res), filename)

        fh = open(filename, "w")
        fh.write(res)

        fh.close()


if __name__ == '__main__':

    download_cboe_volume_all_year()
