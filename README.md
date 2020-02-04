# Python-nCov_Wuhan
一个简单的基于丁香园API的Python爬虫 | A naive python crawler based on API from 丁香园

- 最后更新/Last Updated: 2020.2.3
- Python 3.7 (Anaconda 3)
- 必要Packages:
    - requests
    - pandas
    - json
    - datetime
- 感谢丁香园提供的接口 / Special Acknowledgement to 丁香园 (https://lab.isaaclin.cn/nCoV/)
--------------------------------

# 说明 / Instruction

基于```GET```方法，使用丁香园提供的API获取数据并存储为本地的xlsx文件。目前完成的函数包括：
   1. get_overall(latest)
   2. get_AreaName(abroad)
   3. get_AreaData(area, latest)

### 依赖的Package
```python
import requests
import pandas as pd
import json
import datetime
```

### 使用方法
1. 打开Python 3.7的Console并设置路径
2. 运行nCov2019_crawler.py
3. 按照下方说明使用对应函数

### get_overall(latest)
- 使用下方API接口获取全国的统计量及病毒描述，返回数据类型为```pd.DataFrame```.
> https://lab.isaaclin.cn/nCoV/api/overall

- 功能:
  1. 返回最新的全国统计量及病毒描述，并存储到xlsx. (latest = 1)
  2. 返回全部的全国统计量及病毒描述，并存储到xlsx. (latest = 0)
  
- 举例：

*Input:*

```python
get_overall(1)
```

*Output:*

```python
Processing: Latest information ... 
------------------Success!------------------
Time: 20200203 23_18_36
Filename: nCov2019_overall_20200203 23_18_36.xlsx
Variables: Index(['infectSource', 'passWay', 'dailyPic', 'dailyPics', 'summary',
       'countRemark', 'confirmedCount', 'suspectedCount', 'curedCount',
       'deadCount', 'seriousCount', 'suspectedIncr', 'confirmedIncr',
       'curedIncr', 'deadIncr', 'seriousIncr', 'virus', 'remark1', 'remark2',
       'remark3', 'remark4', 'remark5', 'note1', 'note2', 'note3',
       'generalRemark', 'abroadRemark', 'marquee', 'updateTime'],
      dtype='object')
Data preview:
   infectSource     passWay  ... marquee     updateTime
0   该字段已替换为说明2  该字段已替换为说明3  ...      []  1580789793515
```

### get_AreaName(abroad)
- 使用下方API接口获取目前有数据的国家和地区，返回数据类型为```list```.
> https://lab.isaaclin.cn/nCoV/api/provinceName

- 功能:
  1. 输出当前发现有感染者的省份. (abroad = 0)
  2. 输出当前发现有感染者的除中国外的国家. (abroad = 1)
  3. 输出当前发现有感染者的国家和地区. (abroad = 2)

- 举例:

*Input:*

```python
get_AreaName(1)
```

*Output:*

```python
Regions abroad (26 in Total):  ['俄罗斯', '加拿大', '印度', '尼泊尔', '待明确地区', '德国', '意大利', '斯里兰卡', '新加坡', '日本', '柬埔寨', '法国', '泰国', '澳大利亚', '瑞典', '美国', '芬兰', '英国', '菲律宾', '蒙古', '西班牙', '越南', '阿联酋', '陕西省', '韩国', '马来西亚']
```

### get_AreaData(area, latest)
- 使用下方API接口获取给定区域的详细数据，返回数据类型为```pd.DataFrame```.
> https://lab.isaaclin.cn/nCoV/api/area

- 功能 (*会自动在当前目录创建excel文件存储数据*):
  1. 当latest = 0时返回所有历史数据，当latest = 1时返回最新更新的数据.
  2. 当area = '具体区域'时返回该区域的详细数据，建议结合```get_AreaName(abroad)```使用.
  3. 当area = 'all'时返回当前有数据记录的区域的详细数据.

- 举例:

*Input:*

```python
get_AreaData('广东省', 1)
```

*Output:*

```python
Processing ... url = https://lab.isaaclin.cn/nCoV/api/area?latest=1&province=广东省
------------S------Success!------------------
Time: 20200203 23_28_54
Filename: nCov2019_广东省_20200203 23_28_54.xlsx
Variables: Index(['cityName', 'confirmedCount', 'suspectedCount', 'curedCount',
       'deadCount', 'locationId', 'city', 'country', 'provinceName',
       'provinceShortName', 'comment', 'updateTime', 'createTime',
       'modifyTime', 'province'],
      dtype='object')
Data preview:
   cityName  confirmedCount  suspectedCount  ...  createTime  modifyTime  province
0       深圳             797               0  ...        None        None       NaN
1       广州             797               0  ...        None        None       NaN
2       珠海             797               0  ...        None        None       NaN
3       佛山             797               0  ...        None        None       NaN
4       东莞             797               0  ...        None        None       NaN

[5 rows x 15 columns]
```


------------------------------------
# 原始代码 / Code

```python
# -*- coding: utf-8 -*-
"""
Title:  nCov2019 Virus Data Crawler
Author: DickLiTQ
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
"""------------S------Success!------------------
Time: %s
Filename: nCov2019_%s_%s.xlsx
Variables: %s
Data preview:
"""%(date_time, area, date_time, dataframe.columns), dataframe.head())
    return dataframe
```

