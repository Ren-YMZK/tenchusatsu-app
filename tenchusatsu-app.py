import datetime

# 干支データ
JIKKAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
JUNISHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 十二支→天中殺グループ対応表
SUPPORT_SHI_TO_TENCHUSATSU = {
    "寅": ["申", "酉"], "卯": ["申", "酉"],
    "辰": ["戌", "亥"], "巳": ["戌", "亥"],
    "午": ["子", "丑"], "未": ["子", "丑"],
    "申": ["寅", "卯"], "酉": ["寅", "卯"],
    "戌": ["辰", "巳"], "亥": ["辰", "巳"],
    "子": ["午", "未"], "丑": ["午", "未"]
}

MONTH_TO_JUNISHI = {
    1: "丑", 2: "寅", 3: "卯", 4: "辰", 5: "巳", 6: "午",
    7: "未", 8: "申", 9: "酉", 10: "戌", 11: "亥", 12: "子"
}

# 干支取得


def get_eto_by_index(index):
    return JIKKAN[index % 10] + JUNISHI[index % 12]


def year_to_eto(year):
    base_year = 1984  # 甲子
    diff = year - base_year
    return get_eto_by_index(diff)


def get_nikkanshi_from_birthdate(year, month, day):
    base_date = datetime.date(1984, 2, 2)
    target_date = datetime.date(year, month, day)
    diff = (target_date - base_date).days
    return get_eto_by_index(diff)


def get_user_tenchusatsu_group(user_shi):
    return SUPPORT_SHI_TO_TENCHUSATSU.get(user_shi, [])


def get_all_tenchusatsu_years(user_shi, start_year, end_year):
    tenchusatsu_shi = get_user_tenchusatsu_group(user_shi)
    return [year for year in range(start_year, end_year + 1)
            if year_to_eto(year)[1] in tenchusatsu_shi]


def get_all_tenchusatsu_months(user_shi):
    tenchusatsu_shi = get_user_tenchusatsu_group(user_shi)
    return [month for month, shi in MONTH_TO_JUNISHI.items() if shi in tenchusatsu_shi]


def get_all_tenchusatsu_days(user_shi, year, month):
    tenchusatsu_shi = get_user_tenchusatsu_group(user_shi)
    days = []
    base_date = datetime.date(1984, 2, 2)
    for day in range(1, 32):
        try:
            date = datetime.date(year, month, day)
            diff = (date - base_date).days
            eto = get_eto_by_index(diff)
            if eto[1] in tenchusatsu_shi:
                days.append(f"{day}日（{eto}）")
        except ValueError:
            continue
    return days


# 自動実行用にプリセットデータを定義（インタラクティブ入力なし）
if __name__ == "__main__":
    print("🔮 天中殺チェックアプリ（プリセット版）")

    # プリセット値
    birth_input = "2002-05-08"
    target_year = 2025
    target_month = 4

    birth_year, birth_month, birth_day = map(int, birth_input.split("-"))
    nikkanshi = get_nikkanshi_from_birthdate(
        birth_year, birth_month, birth_day)
    user_shi = nikkanshi[1]

    years = get_all_tenchusatsu_years(
        user_shi, target_year - 5, target_year + 10)
    months = get_all_tenchusatsu_months(user_shi)
    days = get_all_tenchusatsu_days(user_shi, target_year, target_month)

    print(f"\nあなたの日干支：{nikkanshi}")
    print(f"\n天中殺の年（{target_year - 5}〜{target_year + 10}）：{years}")
    month_names = [f"{m}月（{MONTH_TO_JUNISHI[m]}）" for m in months]
    print(f"天中殺の月（毎年共通）：{month_names}")
    print(f"\n{target_year}年{target_month}月の天中殺日：")
    for d in days:
        print(f"- {d}")
