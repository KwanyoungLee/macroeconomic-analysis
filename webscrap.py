from bs4 import BeautifulSoup
import requests
import pandas as pd

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

region_kowloon = [
    ["Olympic_station", 201],
    ["Kowloon_station", 202],
    ["Mongkok_yaumatei", 203],
    ["Tsimshatsui_jordan", 204],
    ["Ho_man_tin_kings_park", 205],
    ["To_ka_wan", 206],
    ["Whampoa_laguna_verde", 207],
    ["Tseung_kwan_o", 209],
    ["Meifoo_wonderland", 210],
    ["Cheung_sha_wan_west", 211],
    ["Cheung_sha_wan_sham_shui_po", 212],
    ["Yau_yat_tsuen_shek_kip_mei", 213],
    ["Kowloon_tong_beacon_hill", 214],
    ["Lam_tin_yau_tong", 215],
    ["Kowloon_bay_ngau_chi_wan", 216],
    ["Kwun_tong", 217],
    ["Diamond_hill_wong_tai_sin", 218],
    ["To_kwa_wan_east", 219],
    ["Hung_hum", 220],
    ["Kai_tak", 221],
]

region_new = [
    ["Sai_kung", 208],
    ["Tai_wai", 301],
    ["Shatin", 302],
    ["Fotan_shatin_mid_level_kau_to_shan", 303],
    ["Ma_on_shan", 304],
    ["Tai_po_mid_level_hong_lok_yuen", 306],
    ["Tai_po_market_tai_wo", 307],
    ["Sheung_shui_fanling_kwu_tung", 308],
]

region_new_east = [
    ["Discovery_bay", 103],
    ["Fairview_park_palm_spring_the_vineyard", 309],
    ["Yuen_long", 401],
    ["Tuen_mun", 402],
    ["Tin_shui_wai", 403 ],
    ["Tsuen_wan", 404],
    ["Kwai_chung", 405 ],
    ["Tsing_yi", 406],
    ["Ma_wan_park_island", 407],
    ["Tung_chung_islands", 408],
    ["Sham_tseng_castle_peak_road", 409],
    ["Belvedere_garden_castle_peak_road", 410],
]

url_front = "http://www1.centadata.com/eptest.aspx?type=22&code="
url_end = "&info=tr&code2=regperiod:1500&page="

def get_property_list():

    for region in region_kowloon:
        page = 0
        file_name = region[0] + ".csv"
        code = region[1]

        print(file_name)
        req = requests.get(f"{url_front}{code}{url_end}{page}")
        soup = BeautifulSoup(req.content, 'html.parser')
        total_item_no = int(soup.find("a", {'name':'txtab'}).find_next_sibling("b").get_text())

        property_list = []
        while page < total_item_no:
            print(page)
            req = requests.get(f"{url_front}{code}{url_end}{page}")
            soup = BeautifulSoup(req.content, 'html.parser')
            content = soup.find_all("table", {'title': 'Detail'})

            for row in content:
                item_list = []
                items = row.find_all("td")
                if len(items) == 10:
                    item_list.append(items[0].get_text())
                    item_list.append(items[1].get_text())
                    item_list.append(items[2].get_text())
                    item_list.append(items[3].get_text().replace("$", "").replace("M", ""))
                    item_list.append(items[4].get_text().replace("s.f.", ""))
                    item_list.append(items[5].get_text().replace("s.f.", ""))
                    item_list.append(items[6].get_text().replace("$", ""))
                    item_list.append(items[7].get_text().replace("$", ""))
                    item_list.append(items[8].get_text().replace("[", "").replace("days", ""))
                    item_list.append(items[9].get_text().replace("]", "").replace("↑", "+").replace("↓", "-").replace("%",""))

                    property_list.append(item_list)
            page += 40

        dataFrame = pd.DataFrame(data=property_list)
        dataFrame.to_csv(file_name)

get_property_list()
#get_page_no()