#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
A test script to fetch weather warnings from JMA without Home Assistant.

Usage:
  python test_script.py [AREA_CODE]

If AREA_CODE is not provided, it defaults to "2710000" (Osaka City).
"""

import asyncio
import sys
import aiohttp

# --- Constants copied from const.py ---
AREA_URL = "https://www.jma.go.jp/bosai/common/const/area.json"
WARNING_URL_FORMAT = "https://www.jma.go.jp/bosai/warning/data/r8/{}.json"
TRANS_WARNING = {
    "02": "暴風雪警報", "03": "大雨警報", "04": "洪水警報", "05": "暴風警報",
    "06": "大雪警報", "07": "波浪警報", "08": "高潮警報", "09": "土砂災害警報",
    "10": "大雨注意報", "12": "大雪注意報", "13": "風雪注意報", "14": "雷注意報",
    "15": "強風注意報", "16": "波浪注意報", "17": "融雪注意報", "18": "洪水注意報",
    "19": "高潮注意報", "20": "濃霧注意報", "21": "乾燥注意報", "22": "なだれ注意報",
    "23": "低温注意報", "24": "霜注意報", "25": "着氷注意報", "26": "着雪注意報",
    "29": "土砂災害注意報", "32": "暴風雪特別警報", "33": "大雨特別警報",
    "35": "暴風特別警報", "36": "大雪特別警報", "37": "波浪特別警報",
    "38": "高潮特別警報", "39": "土砂災害特別警報", "43": "大雨危険警報",
    "48": "高潮危険警報", "49": "土砂災害危険警報",
}
# --- End of constants ---

async def fetch_warnings(session: aiohttp.ClientSession, area_code: str):
    """Fetches and parses weather warnings for a given area code."""
    try:
        # 1. Fetch area information
        print(f"1. Fetching area information for code: {area_code}")
        async with session.get(AREA_URL) as response:
            response.raise_for_status()
            area_data = await response.json()

        class20_info = area_data.get("class20s", {}).get(area_code)
        if not class20_info:
            print(f"Error: Area code '{area_code}' not found in JMA area data.")
            return

        area_name = class20_info["name"]
        class15s_code = class20_info["parent"]
        class10s_code = area_data["class15s"][class15s_code]["parent"]
        office_code = area_data["class10s"][class10s_code]["parent"]
        print(f"   Found area: {area_name}, Office code: {office_code}")

        # 2. Fetch warning information
        print(f"2. Fetching warning data from office: {office_code}")
        warning_url = WARNING_URL_FORMAT.format(office_code)
        async with session.get(warning_url) as response:
            response.raise_for_status()
            warning_info = await response.json()

        # 3. Parse warnings
        print("3. Parsing warning data...")
        warning_codes = []
        for office_warnings in warning_info:
            for class20_item in office_warnings.get("warning", {}).get("class20Items", []):
                if class20_item.get("areaCode") == area_code:
                    for kind in class20_item.get("kinds", []):
                        if kind.get("status") not in ("解除", "発表警報・注意報はなし"):
                            warning_codes.append(kind.get("code"))

        warnings = [TRANS_WARNING.get(code, f"不明なコード: {code}") for code in warning_codes]

        # 4. Display results
        print("\n--- 結果 ---")
        print(f"地域: {area_name} ({area_code})")
        print(f"気象庁情報ページ: https://www.jma.go.jp/bosai/warning/#area_type=class20s&area_code={area_code}&lang=ja")
        if warnings:
            print("発表中の警報・注意報:")
            for warning_text in warnings:
                print(f"- {warning_text}")
        else:
            print("現在、発表されている警報・注意報はありません。")
        print("----------\n")

    except aiohttp.ClientError as err:
        print(f"\nError: Network or API request failed: {err}")
    except Exception as err:
        print(f"\nAn unexpected error occurred: {err}")

async def main():
    """Main function to run the test script."""
    # Use area code from command line argument, or default to Osaka City.
    area_code = sys.argv[1] if len(sys.argv) > 1 else "2710000"

    async with aiohttp.ClientSession() as session:
        await fetch_warnings(session, area_code)

if __name__ == "__main__":
    asyncio.run(main())