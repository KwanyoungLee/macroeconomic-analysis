from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
import math
from datetime import datetime

region_hk = [
    ["Kennedy_town_sai_ying_pun", 101],
    ["South_horizon", 102],
    ["Bel_air_sasson", 104],
    ["Aberdeen_ap_lei_chau", 105],
    ["Mid_level_west", 106],
    ["Peak_south", 107],
    ["Wanchai_causeway_bay", 108],
    ["Mid_level_central", 109],
    ["Happy_valley_mid_level_east", 110],
    ["Mid_level_north_point", 111],
    ["North_point_fortress_hill", 112],
    ["Quarry_bay_kornhill", 113],
    ["Taikoo_shing", 114],
    ["Shau_kei_wan_chai_wan", 115],
    ["Heng_fa_chuen", 116],
    ["Sheung_wan_central_admiralty", 117],
]

url = "https://data.midland.com.hk/search/v1/transactions?"

headers = {
    'Host': 'data.midland.com.hk',
    'Origin': 'https://www.midland.com.hk',
    'authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJndWlkIjoibXItMjAyMS0wMS0wNy1IR0dISy15QlFtYWZRM1hvYjZuMWJ2M2xsa0prVGk4aW9Yd3REOGp6VzBDYTZkLVNZQ0M3M2VYNXJwZUtNYWQzNll1T0RXei1JSSIsImlhdCI6MTYxMDAxMjA2MCwiaXNzIjoiZGF0YS5taWRsYW5kLmNvbS5oayJ9.cCMBWDgWiYriWQqcbnvjjV4c7GaleBcA5rQ9a6alKsSgEwOlCX--fwSt2WsPSHMhNMPVqL58t_zqodmntNOKqZiV4baYXyxpj8AdSL4KufmB5xatdIFKY02mSm-4prcUzBDpNTv0u26hrMQP5wJxx1L4Sag_jx0llqU7WSGKXPKUXHopNvoPb0M05MnjWSnh537yOWRfeWSLmtIdAOWtk3BdlTs8drfuzF969e5dyMCOMSqgz9yOY9liDQfehQsN-9sZSNEU1nyR4EsGW8Nn4yjtppEu9FuYAzrrz2X2NJMO2oagQvsNJoqWw83ktPpf4Tpike5bWkdFCS6g-bz7IMN7X4hslcYd8wmzkIg7Ga5HWqzLU5Ns-1fVkXbulI2HvH109Cn9KlLSPp4Ya2ZCVt5ey5DRMkvQ3jxzJv05CoCfmWVKvxrbOma65t7TPmdYX0OgGH4tl9QRwJZrEoWh7st99cAabs4SKdYO1eKydugP6LXN33fnjayUEH4ouciv0QMRyjocPgGYZSVTBCmS_ks1YHmUB7nm6XzkuuLtzmvBo-PsGTcvfNIIZuonkz4fdTJfZniaU9g-Yp5Ike7517scMLMQLmCJVfDjqbDJ3GQnT_uPEBEiKLpq1in3-xh_o-a0w8wXbmlpJQ488cI67ulc3G8558W9357U1ZbXRvg',
    'Referer': 'https://www.midland.com.hk',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

params = {
    'hash': 'true',
    'lang': 'en',
    'currency': 'HKD',
    'unit': 'feet',
    'search_behavior': 'normal',
    'dist_ids': '100404',
    'tx_type': 'S',
    'tx_date': '3year',
    'page': '1',
    'limit': '50',
}


def get_property_list():

    file_name = "chai_wan.csv"

    req = requests.get(url, headers=headers, params=params)
    soup = BeautifulSoup(req.content, 'html.parser')
    json_data = json.loads(soup.text)

    total_no = json_data["count"]
    print(total_no)

    items = json_data["result"]

    property_list = []
    total_page_no = math.floor(total_no/50)

    for item in items:
        item_list = []

        #region
        item_list.append(item['region']['name'])
        #subregion
        item_list.append(item['subregion']['name'])
        #district
        item_list.append(item['district']['name'])
        #estate
        item_list.append(item['estate']['name'])
        #building
        item_list.append(item['building']['name'])
        #first_op_date
        item_list.append(item['building']['first_op_date'])
        #floor_level
        try:
            item_list.append(item['floor_level']['id'])
        except:
            item_list.append(None)
        #bedroom
        item_list.append(item['bedroom'])
        #sitting_room
        item_list.append(item['sitting_room'])
        #floor
        try:
            item_list.append(item['floor'])
        except:
            item_list.append(None)
        #flat
        item_list.append(item['flat'])
        #area
        item_list.append(item['area'])
        #net_area
        item_list.append(item['net_area'])
        #price
        item_list.append(item['price'])
        #tx_date
        item_list.append(item['price'])
        #last_tx_date
        item_list.append(item['last_tx_date'])
        #last_price
        item_list.append(item['last_price'])
        #gain
        item_list.append(item['gain'])
        #lat
        item_list.append(item['location']['lat'])
        #lon
        item_list.append(item['location']['lon'])

        property_list.append(item_list)

    dataFrame = pd.DataFrame(data=property_list)
    dataFrame.columns = ['region', 'subregion', 'district', 'estate', 'building', 'first_op_date',
                         'floor_level', 'bedroom', 'sitting_room', 'floor', 'flat', 'area', 'net_area',
                         'price', 'tx_date', 'last_tx_date', 'last_price', 'gain', 'lat', 'lon']
    dataFrame.to_csv(file_name)

get_property_list()
