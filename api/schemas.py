from datetime import datetime
from pydantic import BaseModel


class Rikishi(BaseModel):
    id: int
    sumodbId: int | None = None
    nskId: int
    shikonaEn: str
    shikonaJp: str | None = None
    currentRank: str
    heya: str | None = None
    birthDate: datetime | None = None
    shusshin: str | None = None
    height: float
    weight: float
    debut: str
    updatedAt: datetime | None = None
    createdAt: datetime | None = None


class Rikishis(BaseModel):
    limit: int
    skip: int
    total: int
    records: list[Rikishi]


class RikishiStats(BaseModel):
    absenceByDivision: dict[str, int]
    basho: int
    bashoByDivision: dict[str, int]
    lossByDivision: dict[str, int]
    sansho: dict[str, int]
    totalAbsences: int
    totalByDivision: dict[str, int]
    totalLosses: int
    totalMatches: int
    totalWins: int
    winsByDivision: dict[str, int]
    yusho: int
    yushoByDivision: dict[str, int]


class Match(BaseModel):
    id: str
    bashoId: str
    division: str
    day: int
    matchNo: int
    eastId: int
    eastShikona: str
    eastRank: str
    westId: int
    westShikona: str
    westRank: str
    kimarite: str
    winnerId: int
    winnerEn: str
    winnerJp: str


class RikishiMatches(BaseModel):
    limit: int
    skip: int
    total: int
    records: list[Match]


class RikishiVersus(BaseModel):
    kimariteLosses: dict[str, int]
    kimariteWins: dict[str, int]
    matches: list[Match]
    opponentWins: int
    rikishiWins: int
    total: int


class BashoRikishi(BaseModel):
    type: str
    rikishiId: int
    shikonaEn: str
    shikonaJp: str


class SpecialPrize(BaseModel):
    type: str
    rikishiId: int
    shikonaEn: str
    shikonaJp: str


class BashoData(BaseModel):
    date: str
    startDate: datetime
    endDate: datetime
    yusho: list[BashoRikishi] = []
    specialPrizes: list[SpecialPrize]


class BashoBanzukeRikishiRecord(BaseModel):
    result: str
    opponentShikonaEn: str
    opponentShikonaJp: str
    opponentID: int
    kimarite: str


class BashoBanzukeRikishi(BaseModel):
    side: str
    rikishiID: int
    shikonaEn: str
    rankValue: int
    rank: str
    wins: int
    losses: int
    absences: int
    record: list[BashoBanzukeRikishiRecord]


class BashoBanzuke(BaseModel):
    bashoId: str
    division: str
    east: list[BashoBanzukeRikishi]
    west: list[BashoBanzukeRikishi]


class TorikumiYusho(BaseModel):
    type: str
    rikishiId: int
    shikonaEn: str
    shikonaJp: str


class BashoTorikumi(BaseModel):
    date: str
    startDate: str
    endDate: str
    yusho: list[TorikumiYusho]
    specialPrizes: list[SpecialPrize]
    torikumi: list[Match]


# https://www.sumo-api.com/api/kimarite?sortField=count
class Kimarite(BaseModel):
    count: int
    lastUsage: str
    kimarite: str


class Kimarites(BaseModel):
    limit: int
    skip: int
    sortField: str
    sortOrder: str
    records: list[Kimarite]


class KimariteMatches(BaseModel):
    limit: int
    skip: int
    total: int
    records: list[Match]


# # https://www.sumo-api.com/api/measurements?rikishiId=216
# class Measurement(BaseModel):
#     id: str
#     bashoId: str
#     rikishiId: int
#     height: float
#     weight: float


# # IDK IF THIS WORKS
# class Measurements(BaseModel):
#     __root__: list[Measurement]


# # https://www.sumo-api.com/api/ranks?bashoId=202303
# class Rank(BaseModel):
#     id: str
#     bashoId: str
#     rikishiId: int
#     rankValue: int
#     rank: str


# # IDK IF THIS WORKS
# class Ranks(BaseModel):
#     __root__: list[Measurement]


# # https://www.sumo-api.com/api/shikonas?bashoId=202303
# class Shikona(BaseModel):
#     id: str
#     bashoId: str
#     rikishiId: int
#     shikonaEn: str
#     shikonaJp: str


# # IDK IF THIS WORKS
# class Shikonas(BaseModel):
#     __root__: list[Shikona]

