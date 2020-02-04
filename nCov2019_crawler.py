# -*- coding: utf-8 -*-
"""
Title:  nCov2019 Virus Data Crawler
Author: DickLi
Latest Update:   Feb 3, 2020
Method: Get (api)

Special Acknowledgement to 丁香园 (https://lab.isaaclin.cn/nCoV/)
Long may the sun shine.
"""

import requests
import pandas as pd
import json
import datetime

prov_list = list(set(["上海市", "云南省", "内蒙古自治区", "北京市", "台湾", "吉林省", "四川省", "天津市", "宁夏回族自治区", "安徽省", "广东省", "山西省", "山东省", "广西壮族自治区", "新疆维吾尔自治区", "江苏省", "江西省", "河北省", "河南省", "浙江省", "海南省", "湖北省", "湖南省", "澳门", "甘肃省", "福建省", "西藏自治区", "贵州省", "辽宁省", "重庆市", "青海省", "香港", "黑龙江省"]))

def get_overall(latest):
    """ Return data from 4:00pm Jan 24, 2020, datatype: pd.DataFrame """
    """ Get latest info. if latest = 1 """
    """ Get all history if latest = 0  """
    if latest == 1:
        print("Processing: Latest information ... ")
        html = requests.get("https://lab.isaaclin.cn/nCoV/api/overall")
    elif latest == 0:
        print("Processing: Overall information ... ")
        html = requests.get("https://lab.isaaclin.cn/nCoV/api/overall?latest=0")
    else:
        print("Error in option, please choose 1 for latest data or 0 for all history")
        return 0
    if html.status_code != 200:
        print("Error when fetching data! Status code: ", html.status_code)
        return 0
    data_json = json.loads(html.text)
    dataframe = pd.DataFrame(data_json['results'])
    date_time = str(datetime.datetime.now())[:-7]
    date_time = date_time.replace("-","").replace(":","_")
    dataframe.to_excel("nCov2019_overall_%s.xlsx"%date_time)
    print(
"""------------------Success!------------------
Time: %s
Filename: nCov2019_overall_%s.xlsx
Variables: %s
Data preview:
"""%(date_time, date_time, dataframe.columns), dataframe.head())
    return dataframe
    
def get_AreaName(abroad):
    """ Get list of areas, return list """
    """ Only regions in China if abroad = 0 """
    """ Only regions abroad if abroad = 1 """
    """ Regions all over the world if abroad = 2 """
    html = requests.get("https://lab.isaaclin.cn/nCoV/api/provinceName")
    if html.status_code != 200:
        print("Error when fetching data! Status code: ", html.status_code)
        return 0
    data_json = json.loads(html.text)
    AreaName = []
    if abroad == 0:
        for prov in prov_list.sort():
            if prov in data_json['results']:
                AreaName.append(prov)
        print("Regions in China (%d in Total): "%len(AreaName),AreaName)
        return AreaName
    elif abroad == 1:
        AreaName = data_json['results']
        for prov in prov_list:
            if prov in AreaName:
                AreaName.remove(prov)
        print("Regions abroad (%d in Total): "%len(AreaName),AreaName)
        return AreaName
    elif abroad == 2:
        AreaName = data_json['results']
        print("Regions (%d in Total): "%len(AreaName),AreaName)
        return AreaName
    else:
        print("Error in option, please choose 0 for domestic data, 1 for foreign data and 2 for both")
        return 0
   
def get_AreaData(area, latest):
    """ Get data in specific areas, return dataframe """
    """ Fetch all data if area = 'all' """
    """ Get latest info. if latest = 1 """
    """ Get all history if latest = 0  """
    if latest != 0 and latest != 1:
        print("Error in option, please choose 1 for latest data or 0 for all history")
        return 0
    if area == "all":
        url = "https://lab.isaaclin.cn/nCoV/api/area?latest=%d"%latest
    else:
        url = "https://lab.isaaclin.cn/nCoV/api/area?latest=%d&province=%s"%(latest, area)
    print("Processing ... url = %s"%url)
    html = requests.get(url)
    if html.status_code != 200:
        print("Error when fetching data! Status code: ", html.status_code)
        return 0
    data_json = json.loads(html.text)['results']
    data_dict = []
    for item in data_json:
        try: 
            citylist = item['cities']
            item_temp = item.copy()
            del item_temp['cities']
            for i in citylist:
                i.update({'city': 1})
                i.update(item_temp)
                data_dict.append(i)
            item_temp.update({'province': 1})
            data_dict.append(item_temp)
        except:
            data_dict.append(item)
    dataframe = pd.DataFrame(data_dict)
    date_time = str(datetime.datetime.now())[:-7]
    date_time = date_time.replace("-","").replace(":","_")
    dataframe.to_excel("nCov2019_%s_%s.xlsx"%(area, date_time))
    print(
"""------------------Success!------------------
Time: %s
Filename: nCov2019_%s_%s.xlsx
Variables: %s
Data preview:
"""%(date_time, area, date_time, dataframe.columns), dataframe.head())
    return dataframe
