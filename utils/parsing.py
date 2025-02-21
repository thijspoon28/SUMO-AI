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
        "Jonokuchi": 10
    }

    if not rankString:
        return -1

    try:
        x = rankString.split(' ')
        rank = x[0]
        num = x[1]
    
        return rank_order[rank]*100 + int(num)
    
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
