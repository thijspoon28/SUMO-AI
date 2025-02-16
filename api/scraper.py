import time
from api.schemas import BashoBanzukeRikishi
from database.models import Basho, Match, Rikishi, RikishiBasho
from database.queries import Repo
from database.session import get_session
from api.enums import Division
from api.sumo import SumoAPI
import api.schemas as schema



def estimate_iterable(iterable, interval: int = 1, prefix: str = ">"):
    start = time.time()
    prev = time.time()
    cycles = -1
    avg = 0
    maximum = len(iterable)

    x = 0

    print(f"{prefix} Started iterating - {maximum} items")

    for i in iterable:
        yield i
        
        cycles += 1

        cur = time.time()
        spent = cur-prev
        prev = cur

        avg = ((avg * (cycles-1)) + spent) / cycles if cycles > 0 else 0

        estimate = f"{(maximum) * avg:.2f}s"

        if x % interval == 0:
            x = 0
            print(f"{prefix} Cycle {cycles}: elapsed={spent:.2f}s, total={cur-start:.2f}s, estimate={estimate}")

        x += 1


def display_state(info: str, start_time: float, count: int) -> None:
    cur_time = time.time()
    print(f"> {info} - elapsed={cur_time - start_time:.2f}s - record={count}")


def scramble_rikishi(rikishi_id: int) -> Rikishi:
    api = SumoAPI()

    rikishi = api.get_rikishi(rikishi_id)
        
    if not rikishi.currentRank:
        ranks = api.get_ranks(rikishi_id)
        rikishi.currentRank = ranks[0].rank

    if not rikishi.height or not rikishi.weight:
        measurements = api.get_measurements(rikishi_id)
        measurements = measurements if len(measurements) > 0 else [schema.Measurement(id="", bashoId="", rikishiId=0, height=-1, weight=-1)]
        rikishi.height = measurements[0].height
        rikishi.weight = measurements[0].weight
    
    if not rikishi.shikonaEn or not rikishi.shikonaJp:
        shikonas = api.get_shikonas(rikishi_id)
        rikishi.shikonaEn = shikonas[0].shikonaEn
        rikishi.shikonaJp = shikonas[0].shikonaJp

    stat = api.get_rikishi_stats(rikishi_id)

    rikishi_model = Rikishi(
        id=rikishi.id,
        sumodb_id=rikishi.sumodbId,
        nsk_id=rikishi.nskId,
        shikona_en=rikishi.shikonaEn,
        shikona_jp=rikishi.shikonaJp,
        current_rank=rikishi.currentRank,
        heya=rikishi.heya,
        birth_date=rikishi.birthDate,
        shusshin=rikishi.shusshin,
        height=rikishi.height,
        weight=rikishi.weight,
        debut=rikishi.debut,
        intai=rikishi.intai,
        updated_at=rikishi.updatedAt,
        created_at=rikishi.createdAt,

        absence_by_division=stat.absenceByDivision,
        basho_count=stat.basho,
        basho_count_by_division=stat.bashoByDivision,
        loss_by_division=stat.lossByDivision,
        sansho=stat.sansho,
        total_absences=stat.totalAbsences,
        total_by_division=stat.totalByDivision,
        total_losses=stat.totalLosses,
        total_matches=stat.totalMatches,
        total_wins=stat.totalWins,
        wins_by_division=stat.winsByDivision,
        yusho_count=stat.yusho,
        yusho_count_by_division=stat.yushoByDivision,
    )
    
    return rikishi_model


def scrape_basho(basho_id: str, division: Division | str) -> None:
    api = SumoAPI()
    session = get_session()
    start_time = time.time()

    division = division.value if isinstance(division, Division) else division

    basho = api.get_basho(basho_id)
    basho_benzuke = api.get_basho_banzuke(basho_id, division)

    count = 0

    basho_model = Repo.find_basho(basho_id)
    if basho_model is None:
        basho_model = Basho(
            id=basho_id,
            date=basho.date,
            start_date=basho.startDate,
            end_date=basho.endDate,
        )
        count += 1
        session.add(basho_model)

    # Empty kimarite filler
    common_kimarite = api.get_kimarite().records[-1]

    yusho = {yu.rikishiId: yu.type for yu in basho.yusho}
    special_prize = {sp.rikishiId: sp.type for sp in basho.specialPrizes}

    rikishis: list[BashoBanzukeRikishi] = basho_benzuke.east + basho_benzuke.west

    for banzuke_rikishi in estimate_iterable(rikishis, 1):
        r = Repo.find_rikishi(banzuke_rikishi.rikishiID)

        if r is None:
            r = scramble_rikishi(banzuke_rikishi.rikishiID)

            rik_bas = RikishiBasho(
                rikishi_id=r.id,
                basho_id=basho_id,
                special_prize=special_prize.get(r.id),
                yusho=yusho.get(r.id),
            )

            session.add(r)
            session.add(rik_bas)

            count += 2

        for match_ in banzuke_rikishi.record:
            if match_.opponentID == 0:
                continue

            if (
                Repo.find_match(basho_id, division, r.id, match_.opponentID)
                is not None
            ):
                continue

            rikishi_matches = api.get_rikishi_versus(
                r.id,
                match_.opponentID,
                # basho_id,
                # scrape=True,
            )

            for rm in rikishi_matches.matches:
                if (
                    Repo.find_match(rm.bashoId, rm.division, rm.eastId, rm.westId)
                    is not None
                ):
                    continue
                new = Match(
                    basho_id=rm.bashoId,
                    division=division,
                    day=rm.day,
                    match_no=rm.matchNo,
                    east_id=rm.eastId,
                    east_shikona=rm.eastShikona,
                    east_rank=rm.eastRank,
                    west_id=rm.westId,
                    west_shikona=rm.westShikona,
                    west_rank=rm.westRank,
                    kimarite=rm.kimarite if rm.kimarite != "" else common_kimarite.kimarite,
                    winner_id=rm.winnerId,
                    winner_en=rm.winnerEn,
                    winner_jp=rm.winnerJp,
                )
                session.add(new)

                count += 1

        session.commit()

    display_state("Finished scrape", start_time, count)


def scrape_all(limit: int | None = None):
    api = SumoAPI()
    session = get_session()

    # Get all rikishi
    #   - Get stats
    #   - Get all ranks
    #   - Get all measurements
    #   - Get all shikonas

    rikishis = api.get_rikishis(
        measurements=True,
        ranks=True,
        shikonas=True,
        limit=limit,
    )

    rikishi_models: list[Rikishi] = []

    for rikishi in rikishis.records:
        r = scramble_rikishi(rikishi.id)

        session.add(r)
        session.refresh(r)

        rikishi_models.append(r)

    # Get all busho

    # Get all kimarite
    # Get all matches per kimarite
    # Match all matches with rikishi
