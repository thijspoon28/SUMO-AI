from api.schemas import BashoBanzukeRikishi
from database.models import Basho, Match, Rikishi, RikishiBasho
from database.queries import Repo
from database.session import get_session
from api.enums import Division
from api.sumo import SumoAPI
import api.schemas as schema
from utils.estimate import estimate


def scramble_rikishi(rikishi_id: int) -> Rikishi:
    api = SumoAPI()

    rikishi_r = api.get_rikishi(rikishi_id)
    stat_r = api.get_rikishi_stats(rikishi_id)

    assert rikishi_r.record is not None
    assert stat_r.record is not None

    stat: schema.RikishiStats = stat_r.record
    rikishi: schema.Rikishi = rikishi_r.record

    if not rikishi.currentRank:
        ranks_r = api.get_ranks(rikishi_id)
        ranks: list[schema.Rank] = ranks_r.records if ranks_r.length > 0 else [schema.Rank(id="", bashoId="", rikishiId=0, rank="Unranked", rankValue=9999)]  # type: ignore
        rikishi.currentRank = ranks[0].rank

    if not rikishi.height or not rikishi.weight:
        measurements_r = api.get_measurements(rikishi_id)
        measurements: list[schema.Measurement] = measurements_r.records if measurements_r.length > 0 else [schema.Measurement(id="", bashoId="", rikishiId=0, height=-1, weight=-1)]  # type: ignore
        rikishi.height = measurements[0].height
        rikishi.weight = measurements[0].weight

    if not rikishi.shikonaEn or not rikishi.shikonaJp:
        shikonas_r = api.get_shikonas(rikishi_id)
        shikonas: list[schema.Shikona] = shikonas_r.records if shikonas_r.length > 0 else [schema.Shikona(id="", bashoId="", rikishiId=0, shikonaEn="No name", shikonaJp="No name")]  # type: ignore
        rikishi.shikonaEn = shikonas[0].shikonaEn
        rikishi.shikonaJp = shikonas[0].shikonaJp

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

    division = division.value if isinstance(division, Division) else division

    basho_r = api.get_basho(basho_id)
    basho_banzuke_r = api.get_basho_banzuke(basho_id, division)

    assert basho_r.record is not None
    assert basho_banzuke_r.record is not None

    basho = basho_r.record
    basho_banzuke = basho_banzuke_r.record

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
    kimarites_r = api.get_kimarite()
    assert kimarites_r.records is not None

    common_kimarite = kimarites_r.records[-1]

    if basho.yusho is None:
        basho.yusho = []
    if basho.specialPrizes is None:
        basho.specialPrizes = []

    yusho = {yu.rikishiId: yu.type for yu in basho.yusho}
    special_prize = {sp.rikishiId: sp.type for sp in basho.specialPrizes}

    if basho_banzuke.east is None:
        basho_banzuke.east = []
    if basho_banzuke.west is None:
        basho_banzuke.west = []

    rikishis: list[BashoBanzukeRikishi] = basho_banzuke.east + basho_banzuke.west

    for banzuke_rikishi in estimate(rikishis, title="Rikishi"):
        r = Repo.find_rikishi(banzuke_rikishi.rikishiID)

        if r is None:
            r = scramble_rikishi(banzuke_rikishi.rikishiID)

            rik_bas = RikishiBasho(
                rikishi_id=r.id,
                basho_id=basho_id,
                special_prize=special_prize.get(int(r.id)),
                yusho=yusho.get(int(r.id)),
            )

            session.add(r)
            session.add(rik_bas)

            count += 2

        if banzuke_rikishi.record is None:
            banzuke_rikishi.record = []

        for match_ in banzuke_rikishi.record:
            if match_.opponentID == 0:
                continue

            if (
                Repo.find_match(basho_id, division, int(r.id), match_.opponentID)
                is not None
            ):
                continue

            rikishi_matches_r = api.get_rikishi_versus(
                int(r.id),
                match_.opponentID,
            )
            assert rikishi_matches_r.record is not None

            for rm in rikishi_matches_r.record.matches:
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
                    kimarite=(
                        rm.kimarite if rm.kimarite != "" else common_kimarite.kimarite
                    ),
                    winner_id=rm.winnerId,
                    winner_en=rm.winnerEn,
                    winner_jp=rm.winnerJp,
                )
                session.add(new)

                count += 1

        session.commit()


def scrape_all(limit: int | None = None):
    api = SumoAPI()
    session = get_session()

    # Get all rikishi
    #   - Get stats
    #   - Get all ranks
    #   - Get all measurements
    #   - Get all shikonas

    rikishis_r = api.get_rikishis(
        measurements=True,
        ranks=True,
        shikonas=True,
        limit=limit,
    )
    assert rikishis_r.records is not None

    rikishi_models: list[Rikishi] = []
    rikishis = rikishis_r.records

    for rikishi in rikishis:
        r = scramble_rikishi(rikishi.id)

        session.add(r)
        session.refresh(r)

        rikishi_models.append(r)

    # Get all busho

    # Get all kimarite
    # Get all matches per kimarite
    # Match all matches with rikishi
