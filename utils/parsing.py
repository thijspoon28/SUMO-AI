def sumo_rank_to_value(rankString: str | None = None, **kwargs) -> int:
    rank_order = {
        "Yokozuna": 1,
        "Ozeki": 2,
        "Sekiwake": 3,
        "Komusubi": 4,
        "Maegashira": 5,
        "Juryo": 6,
        "Makushita": 7,
        "Sandanme": 8,
        "Jonidan": 9,
        "Jonokuchi": 10,
    }

    if not rankString:
        return -1

    try:
        x = rankString.split(" ")
        rank = x[0]
        num = x[1]

        return rank_order[rank] * 100 + int(num)

    except Exception as exc:
        print(rankString, exc)
        return 9999


def next_basho_id(basho_id: str) -> str:
    year = int(basho_id[:4])
    month = int(basho_id[4:])

    month += 2

    if month > 12:
        month = 1
        year += 1

    return f"{year}{month:0>{2}}"


def prev_basho_id(basho_id: str) -> str:
    year = int(basho_id[:4])
    month = int(basho_id[4:])

    month -= 2

    if month < 0:
        month = 11
        year -= 1

    return f"{year}{month:0>{2}}"


def next_basho_date(basho_date: tuple[str, int]) -> tuple[str, int]:
    basho_id = basho_date[0]
    day = basho_date[1]

    day += 1

    if day > 15:
        day = 1
        basho_id = next_basho_id(basho_id)

    return basho_id, day


def prev_basho_date(basho_date: tuple[str, int]) -> tuple[str, int]:
    basho_id = basho_date[0]
    day = basho_date[1]

    day -= 1

    if day < 1:
        day = 15
        basho_id = prev_basho_id(basho_id)

    return basho_id, day


def value_to_kimarite(kimarite_value: int) -> str:
    kimarite_map = {
        1: "yorikiri",
        2: "oshidashi",
        3: "",
        4: "hatakikomi",
        5: "uwatenage",
        6: "yoritaoshi",
        7: "tsukiotoshi",
        8: "hikiotoshi",
        9: "oshitaoshi",
        10: "shitatenage",
        11: "okuridashi",
        12: "sukuinage",
        13: "tsukidashi",
        14: "kotenage",
        15: "uwatedashinage",
        16: "tsuridashi",
        17: "katasukashi",
        18: "sotogake",
        19: "fusen",
        20: "utchari",
        21: "okuritaoshi",
        22: "shitatedashinage",
        23: "abisetaoshi",
        24: "kirikaeshi",
        25: "kimedashi",
        26: "tsukitaoshi",
        27: "kubinage",
        28: "shitatehineri",
        29: "isamiashi",
        30: "kakenage",
        31: "tottari",
        32: "uchigake",
        33: "uwatehineri",
        34: "hikkake",
        35: "kainahineri",
        36: "makiotoshi",
        37: "kimetaoshi",
        38: "watashikomi",
        39: "ashitori",
        40: "kekaeshi",
        41: "ketaguri",
        42: "uchimuso",
        43: "komatasukui",
        44: "susoharai",
        45: "amiuchi",
        46: "tsukihiza",
        47: "okurinage",
        48: "sokubiotoshi",
        49: "dashinage",
        50: "koshikudake",
        51: "hansoku",
        52: "nichonage",
        53: "tsukite",
        54: "zubuneri",
        55: "chongake",
        56: "harimanage",
        57: "kawazugake",
        58: "sakatottari",
        59: "tsuriotoshi",
        60: "kubihineri",
        61: "fumidashi",
        62: "nimaigeri",
        63: "ipponzeoi",
        64: "sotokomata",
        65: "okurihikiotoshi",
        66: "sabaori",
        67: "tokkurinage",
        68: "ushiromotare",
        69: "izori",
        70: "kotehineri",
        71: "waridashi",
        72: "osakate",
        73: "yaguranage",
        74: "sotomuso",
        75: "gasshohineri",
        76: "tsutaezori",
        77: "koshinage",
        78: "susotori",
        79: "tasukizori",
        80: "yobimodoshi",
        81: "kozumatori",
        82: "mitokorozeme",
        83: "okuritsuridashi",
        84: "okuritsuriotoshi",
        85: "tsumatori",
        86: "hikiwake",
        87: "omata",
        88: "okurigake",
        89: "itamiwake",
        90: "tsukaminage",
        91: "yobikaeshi",
    }

    return kimarite_map[kimarite_value]


def kimarite_to_value(kimarite: str) -> int:
    kimarite_map = {
        "yorikiri": 1,
        "oshidashi": 2,
        "": 3,
        "hatakikomi": 4,
        "uwatenage": 5,
        "yoritaoshi": 6,
        "tsukiotoshi": 7,
        "hikiotoshi": 8,
        "oshitaoshi": 9,
        "shitatenage": 10,
        "okuridashi": 11,
        "sukuinage": 12,
        "tsukidashi": 13,
        "kotenage": 14,
        "uwatedashinage": 15,
        "tsuridashi": 16,
        "katasukashi": 17,
        "sotogake": 18,
        "fusen": 19,
        "utchari": 20,
        "okuritaoshi": 21,
        "shitatedashinage": 22,
        "abisetaoshi": 23,
        "kirikaeshi": 24,
        "kimedashi": 25,
        "tsukitaoshi": 26,
        "kubinage": 27,
        "shitatehineri": 28,
        "isamiashi": 29,
        "kakenage": 30,
        "tottari": 31,
        "uchigake": 32,
        "uwatehineri": 33,
        "hikkake": 34,
        "kainahineri": 35,
        "makiotoshi": 36,
        "kimetaoshi": 37,
        "watashikomi": 38,
        "ashitori": 39,
        "kekaeshi": 40,
        "ketaguri": 41,
        "uchimuso": 42,
        "komatasukui": 43,
        "susoharai": 44,
        "amiuchi": 45,
        "tsukihiza": 46,
        "okurinage": 47,
        "sokubiotoshi": 48,
        "dashinage": 49,
        "koshikudake": 50,
        "hansoku": 51,
        "nichonage": 52,
        "tsukite": 53,
        "zubuneri": 54,
        "chongake": 55,
        "harimanage": 56,
        "kawazugake": 57,
        "sakatottari": 58,
        "tsuriotoshi": 59,
        "kubihineri": 60,
        "fumidashi": 61,
        "nimaigeri": 62,
        "ipponzeoi": 63,
        "sotokomata": 64,
        "okurihikiotoshi": 65,
        "sabaori": 66,
        "tokkurinage": 67,
        "ushiromotare": 68,
        "izori": 69,
        "kotehineri": 70,
        "waridashi": 71,
        "osakate": 72,
        "yaguranage": 73,
        "sotomuso": 74,
        "gasshohineri": 75,
        "tsutaezori": 76,
        "koshinage": 77,
        "susotori": 78,
        "tasukizori": 79,
        "yobimodoshi": 80,
        "kozumatori": 81,
        "mitokorozeme": 82,
        "okuritsuridashi": 83,
        "okuritsuriotoshi": 84,
        "tsumatori": 85,
        "hikiwake": 86,
        "omata": 87,
        "okurigake": 88,
        "itamiwake": 89,
        "tsukaminage": 90,
        "yobikaeshi": 91,
    }

    return kimarite_map[kimarite]
