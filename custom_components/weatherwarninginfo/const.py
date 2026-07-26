"""Constants for the JMA Weather Warning Info integration."""

DOMAIN = "weatherwarninginfo"

# JMA URLs
AREA_URL = "https://www.jma.go.jp/bosai/common/const/area.json"
WARNING_URL_FORMAT = "https://www.jma.go.jp/bosai/warning/data/r8/{}.json"

# Configuration
CONF_AREA_CODE = "area_code"

# Warning code to name translation
TRANS_WARNING = {
    "02": "暴風雪警報",
    "03": "大雨警報",
    "04": "洪水警報",
    "05": "暴風警報",
    "06": "大雪警報",
    "07": "波浪警報",
    "08": "高潮警報",
    "09": "土砂災害警報",
    "10": "大雨注意報",
    "12": "大雪注意報",
    "13": "風雪注意報",
    "14": "雷注意報",
    "15": "強風注意報",
    "16": "波浪注意報",
    "17": "融雪注意報",
    "18": "洪水注意報",
    "19": "高潮注意報",
    "20": "濃霧注意報",
    "21": "乾燥注意報",
    "22": "なだれ注意報",
    "23": "低温注意報",
    "24": "霜注意報",
    "25": "着氷注意報",
    "26": "着雪注意報",
    "29": "土砂災害注意報",
    "32": "暴風雪特別警報",
    "33": "大雨特別警報",
    "35": "暴風特別警報",
    "36": "大雪特別警報",
    "37": "波浪特別警報",
    "38": "高潮特別警報",
    "39": "土砂災害特別警報",
    "43": "大雨危険警報",
    "48": "高潮危険警報",
    "49": "土砂災害危険警報",
}
