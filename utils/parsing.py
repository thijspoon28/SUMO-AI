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
