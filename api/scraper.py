from datetime import datetime
import time
from api.schemas import BashoBanzukeRikishi
from database.models import Basho, Match, Rikishi, RikishiBasho
from database.queries import find_basho, find_match
from database.session import get_session
from api.enums import Division
from api.sumo import SumoAPI
import api.schemas as schema




def display_state(info: str, start_time: float, count: int) -> None:
    cur_time = time.time()
    print(f"> {info} - elapsed={cur_time - start_time:.2f}s - count={count}")


def scramble_rikishi(rikishi_id: int) -> Rikishi:
    api = SumoAPI()

    is_available = True

    try:
        rikishi = api.get_rikishi(rikishi_id)
        
    except Exception:
        is_available = False
        ranks = api.get_ranks(rikishi_id)

        measurements = api.get_measurements(rikishi_id)
        measurements = measurements if len(measurements) > 0 else [schema.Measurement(id="", bashoId="", rikishiId=0, height=-1, weight=-1)]
        
        shikonas = api.get_shikonas(rikishi_id)

    stat = api.get_rikishi_stats(rikishi_id)

    if is_available:
        rikishi_model = Rikishi(
            id=rikishi.id,
            sumodb_id=rikishi.sum,
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
    
    else:
        rikishi_model = Rikishi(
            id=rikishi_id,
            sumodb_id=-1,
            nsk_id=-1,
            shikona_en=shikonas[0].shikonaEn,
            shikona_jp=shikonas[0].shikonaJp,
            current_rank=ranks[0].rank,
            heya="Retired",
            birth_date=datetime.min,
            shusshin="Retired",
            height=measurements[0].height,
            weight=measurements[0].weight,
            debut="Retired",
            intai=datetime.min,
            updated_at=None,
            created_at=None,

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

    count = 1

    basho_model = find_basho(basho_id)
    if basho_model is None:
        basho_model = Basho(
            id=basho_id,
            date=basho.date,
            start_date=basho.startDate,
            end_date=basho.endDate,
        )
        session.add(basho_model)
    
    display_state("Retrieved Basho", start_time, count)

    yusho = {yu.rikishiId: yu.type for yu in basho.yusho}
    special_prize = {sp.rikishiId: sp.type for sp in basho.specialPrizes}

    rikishis: list[BashoBanzukeRikishi] = basho_benzuke.east + basho_benzuke.west

    for banzuke_rikishi in rikishis:
        r = scramble_rikishi(banzuke_rikishi.rikishiID)

        rik_bas = RikishiBasho(
            rikishi_id=r.id,
            basho_id=basho_id,
            special_prize=special_prize.get(r.id),
            yusho=yusho.get(r.id),
        )

        rik_bas.rikishi = r
        rik_bas.basho = basho_model

        session.add(r)
        session.add(rik_bas)

        count += 2
        display_state(f"Added Rikishi({r.id})", start_time, count)

        for match_ in banzuke_rikishi.record:
            if match_.opponentID == 0:
                new = Match(
                    basho_id=basho_id,
                    division=division,
                    day=-1,
                    match_no=-1,
                    east_id=-1,
                    east_shikona="Absent",
                    east_rank="Absent",
                    west_id=-1,
                    west_shikona="Absent",
                    west_rank="Absent",
                    kimarite="Absent",
                    winner_id=-1,
                    winner_en="Absent",
                    winner_jp="Absent",
                )
                session.add(new)

                count += 1
                display_state("Added match", start_time, count)

                continue
            if (
                find_match(basho_id, division, r.id, match_.opponentID)
                is not None
            ):
                continue

            rikishi_matches = api.get_rikishi_versus(
                r.id,
                match_.opponentID,
                basho_id,
                # scrape=True,
            )

            for rm in rikishi_matches.matches:
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
                    kimarite=rm.kimarite,
                    winner_id=rm.winnerId,
                    winner_en=rm.winnerEn,
                    winner_jp=rm.winnerJp,
                )
                session.add(new)

                count += 1
                display_state("Added match", start_time, count)

    display_state("Finished scrape", start_time, count)
    input(f"Inputting {count} records into the database. Press ENTER to proceed.")
    print("Comminting...")
    session.commit()
    print("Fin.")


def scrape_api(limit: int | None = None):
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
        stat = api.get_rikishi_stats(rikishi.id)

        r = Rikishi(
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

        session.add(r)
        session.refresh(r)

        rikishi_models.append(r)

    # Get all busho

    # Get all kimarite
    # Get all matches per kimarite
    # Match all matches with rikishi
