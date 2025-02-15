from api.schemas import BashoBanzukeRikishi
from database.models import Basho, Match, Rikishi
from database.queries import find_match
from database.session import get_session
from api.enums import Division
from api.sumo import SumoAPI


def scrape_basho(basho_id: str, division: Division | str):
    api = SumoAPI()
    session = get_session()

    division = division if isinstance(division, str) else division.value

    basho = api.get_basho(basho_id)
    basho_benzuke = api.get_basho_banzuke(basho_id, division)

    basho_model = Basho(
        id=basho_id,
        date=basho.date,
        start_date=basho.startDate,
        end_date=basho.endDate,
    )

    rikishis: list[BashoBanzukeRikishi] = basho_benzuke.east + basho_benzuke.west

    for rikishi in rikishis:
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

        

        for match_ in rikishi.record:
            if (
                find_match(basho_id, division, rikishi.rikishiID, match_.opponentID)
                is not None
            ):
                continue

            rikishi_matches = api.get_rikishi_versus(
                rikishi.rikishiID,
                match_.opponentID,
                basho_id,
                scrape=True,
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
