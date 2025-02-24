from pydantic import ValidationError
from core.external_api.response_schemas import BashoResponse
from core.db.models import (
    Basho,
    Match,
    Measurement,
    Rank,
    Rikishi,
    RikishiBasho,
    Shikona,
)
from database.queries import Repo
from core.db import get_session
from core.external_api.enums import Division
from core.external_api.sumo import SumoAPI
import core.external_api.schemas as schema
from core.helpers.utils.estimate import estimate


def log_missing_rikishi(rikishi_id: int):
    with open("data/missing_rikishi.txt", "a") as f:
        f.write(f"{rikishi_id}\n")


def include(
    rikishi: Rikishi,
    ranks: list[schema.Rank] = [],
    measurements: list[schema.Measurement] = [],
    shikonas: list[schema.Shikona] = [],
) -> Rikishi:
    for r in ranks:
        model = Rank(
            basho_id=r.bashoId,
            rikishi_id=r.rikishiId,
            rank_value=r.rankValue,
            rank=r.rank,
        )

        rikishi.rankHistory.append(model)

    for m in measurements:
        model = Measurement(
            basho_id=m.bashoId,
            rikishi_id=m.rikishiId,
            height=m.height,
            weight=m.weight,
        )

        rikishi.measurementHistory.append(model)

    for s in shikonas:
        model = Shikona(
            basho_id=s.bashoId,
            rikishi_id=s.rikishiId,
            shikona_en=s.shikonaEn,
            shikona_jp=s.shikonaJp,
        )

        rikishi.shikonaHistory.append(model)

    return rikishi


def rikishi_ranks(rikishi_id: int, scrape: bool = False):
    api = SumoAPI()
    ranks_r = api.get_ranks(rikishi_id, scrape=scrape)
    ranks: list[schema.Rank] = ranks_r.records if ranks_r.length > 0 else [schema.Rank(id="", bashoId="", rikishiId=0, rank="Unranked", rankValue=9999)]  # type: ignore
    return ranks


def rikishi_measurements(rikishi_id: int, scrape: bool = False):
    api = SumoAPI()
    measurements_r = api.get_measurements(rikishi_id, scrape=scrape)
    measurements: list[schema.Measurement] = measurements_r.records if measurements_r.length > 0 else [schema.Measurement(id="", bashoId="", rikishiId=0, height=-1, weight=-1)]  # type: ignore
    return measurements


def rikishi_shikonas(rikishi_id: int, scrape: bool = False):
    api = SumoAPI()
    shikonas_r = api.get_shikonas(rikishi_id, scrape=scrape)
    shikonas: list[schema.Shikona] = shikonas_r.records if shikonas_r.length > 0 else [schema.Shikona(id="", bashoId="", rikishiId=0, shikonaEn="No name", shikonaJp="No name")]  # type: ignore
    return shikonas


def create_missing_rikishi(rikishi_id: int):
    rikishi = scramble_rikishi(rikishi_id, True, True, True)

    session = get_session()
    session.add(rikishi)
    session.close()


def scramble_rikishi(
    rikishi_id: int,
    incl_measurements: bool = False,
    incl_ranks: bool = False,
    incl_shikonas: bool = False,
) -> Rikishi:
    api = SumoAPI()

    rikishi_r = api.get_rikishi(
        rikishi_id,
        incl_measurements,
        incl_ranks,
        incl_shikonas,
    )
    stat_r = api.get_rikishi_stats(rikishi_id)

    assert rikishi_r.record is not None
    assert stat_r.record is not None

    stat: schema.RikishiStats = stat_r.record
    rikishi: schema.Rikishi = rikishi_r.record

    if incl_ranks or not rikishi.currentRank:
        ranks = rikishi_ranks(rikishi_id, scrape=incl_ranks)
        rikishi.currentRank = ranks[0].rank

    if incl_measurements or not rikishi.height or not rikishi.weight:
        measurements = rikishi_measurements(rikishi_id, scrape=incl_measurements)
        rikishi.height = measurements[0].height
        rikishi.weight = measurements[0].weight

    if incl_shikonas or not rikishi.shikonaEn or not rikishi.shikonaJp:
        shikonas = rikishi_shikonas(rikishi_id, scrape=incl_shikonas)
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

    if incl_measurements:
        rikishi_model = include(rikishi_model, measurements=measurements)

    if incl_ranks:
        rikishi_model = include(rikishi_model, ranks=ranks)

    if incl_shikonas:
        rikishi_model = include(rikishi_model, shikonas=shikonas)

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

    basho_model = Repo.find_basho(session, basho_id)
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

    rikishis: list[schema.BashoBanzukeRikishi] = basho_banzuke.east + basho_banzuke.west

    for banzuke_rikishi in estimate(rikishis, title="Rikishi"):
        r = Repo.find_rikishi(session, banzuke_rikishi.rikishiID)

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
                Repo.find_basho_versus(session, basho_id, int(r.id), match_.opponentID)
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
                    Repo.find_match(session, rm.bashoId, rm.day, rm.eastId, rm.westId)
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


def scrape_all():
    api = SumoAPI()
    session = get_session()

    rikishis_r = api.get_rikishis(scrape=True, skip=6312)
    assert rikishis_r.records is not None

    basho_data: dict[str, BashoResponse] = {}  # type: ignore

    for rikishi in estimate(rikishis_r.records, title="Rikishi", disable_terminal_chomp_chomp=False):
        r = Repo.find_rikishi(session, rikishi.id)

        if r is None:
            r = scramble_rikishi(rikishi.id, True, True, True)

            try:
                schema.ValidateRikishi.model_validate(r)

            except ValidationError:
                log_missing_rikishi(rikishi.id)
                continue

            else:
                session.add(r)

        else:
            x = []
            if not r.measurementHistory:
                r = include(r, measurements=rikishi_measurements(r.id))
                x.append("Measurement")

            if not r.rankHistory:
                r = include(r, ranks=rikishi_ranks(r.id))
                x.append("Rank")

            if not r.shikonaHistory:
                r = include(r, shikonas=rikishi_shikonas(r.id))
                x.append("Shikona")

            if len(x) > 0:
                print(f"Retrieved {x} histories.")

        print(f"Rikishi: ({rikishi.id}) {r.shikona_en}")

        matches_r = api.get_rikishi_matches(r.id, scrape=True)
        assert matches_r.records is not None

        for km in estimate(matches_r.records, title="Matches"):
            if not basho_data.get(km.bashoId):
                basho_r = api.get_basho(km.bashoId)
                basho_data[km.bashoId] = basho_r

            else:
                basho_r = basho_data[km.bashoId]

            assert basho_r.record is not None

            if Repo.find_basho(session, km.bashoId) is None:
                b = Basho(
                    id=km.bashoId,
                    date=basho_r.record.date,
                    start_date=basho_r.record.startDate,
                    end_date=basho_r.record.endDate,
                )

                print(f"Added basho {km.bashoId}")
                session.add(b)

            if Repo.find_rikishi_basho(session, km.bashoId, rikishi.id) is None:
                # Get special prize and yusho
                sp = next(
                    (
                        d.type
                        for d in basho_r.record.specialPrizes
                        if d.rikishiId == rikishi.id
                    ),
                    None,
                )
                yu = next(
                    (
                        d.type
                        for d in basho_r.record.yusho
                        if d.rikishiId == rikishi.id
                    ),
                    None,
                )

                rb = RikishiBasho(
                    rikishi_id=rikishi.id,
                    basho_id=km.bashoId,
                    special_prize=sp,
                    yusho=yu,
                )

                print(f"Added basho_rikishi {rb.basho_id}-{rb.rikishi_id}, sp={rb.special_prize}, yu={rb.yusho}")
                session.add(rb)

            if (
                Repo.find_match(session, km.bashoId, km.day, km.eastId, km.westId)
                is None
            ):
                m = Match(
                    basho_id=km.bashoId,
                    division=km.division,
                    day=km.day,
                    match_no=km.matchNo,
                    east_id=km.eastId,
                    east_shikona=km.eastShikona,
                    east_rank=km.eastRank,
                    west_id=km.westId,
                    west_shikona=km.westShikona,
                    west_rank=km.westRank,
                    kimarite=km.kimarite,
                    winner_id=km.winnerId,
                    winner_en=km.winnerEn,
                    winner_jp=km.winnerJp,
                )

                msg = f"{km.bashoId}-{km.day} east={km.eastId} vs west={km.westId}"
                print(f"Added match ({msg})")
                session.add(m)

        print("\n")
        session.commit()
