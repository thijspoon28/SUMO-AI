from datetime import datetime
from pydantic import BaseModel


class Measurement(BaseModel):
    id: str
    bashoId: str
    rikishiId: int
    height: float
    weight: float


class Rank(BaseModel):
    id: str
    bashoId: str
    rikishiId: int
    rankValue: int
    rank: str


class Shikona(BaseModel):
    id: str
    bashoId: str
    rikishiId: int
    shikonaEn: str
    shikonaJp: str | None = None


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
    winnerJp: str | None = None


# Yes, this is the same as Match above, just missing the Id
class RikishiMatch(BaseModel):
    # id: str
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
    winnerJp: str | None = None


class BashoRikishi(BaseModel):
    type: str
    rikishiId: int
    shikonaEn: str
    shikonaJp: str | None = None


class SpecialPrize(BaseModel):
    type: str
    rikishiId: int
    shikonaEn: str | None = None
    shikonaJp: str | None = None


class BashoBanzukeRikishiRecord(BaseModel):
    result: str
    opponentShikonaEn: str
    opponentShikonaJp: str | None = None
    opponentID: int
    kimarite: str


class TorikumiYusho(BaseModel):
    type: str
    rikishiId: int
    shikonaEn: str | None = None
    shikonaJp: str | None = None


class Kimarite(BaseModel):
    count: int
    lastUsage: str
    kimarite: str


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
    measurementHistory: list[Measurement] | None = []
    rankHistory: list[Rank] | None = []
    shikonaHistory: list[Shikona] | None = []
    height: float
    weight: float
    debut: str
    intai: datetime | None = None
    updatedAt: datetime | None = None
    createdAt: datetime | None = None


class RikishiVersus(BaseModel):
    kimariteLosses: dict[str, int]
    kimariteWins: dict[str, int]
    matches: list[RikishiMatch]
    opponentWins: int
    rikishiWins: int
    total: int


class BashoData(BaseModel):
    date: str
    startDate: datetime
    endDate: datetime
    yusho: list[BashoRikishi] | None = []
    specialPrizes: list[SpecialPrize] | None = []


class BashoBanzukeRikishi(BaseModel):
    side: str
    rikishiID: int
    shikonaEn: str
    rankValue: int
    rank: str
    wins: int
    losses: int
    absences: int
    record: list[BashoBanzukeRikishiRecord] | None = []


class BashoBanzuke(BaseModel):
    bashoId: str
    division: str
    east: list[BashoBanzukeRikishi] | None = []
    west: list[BashoBanzukeRikishi] | None = []


class KimariteResponse(BaseModel):
    limit: int
    skip: int
    sortField: str
    sortOrder: str
    records: list[Kimarite] | None = []


class BashoTorikumi(BaseModel):
    date: str
    startDate: str
    endDate: str
    yusho: list[TorikumiYusho] | None = []
    specialPrizes: list[SpecialPrize] | None = []
    torikumi: list[Match] | None = []


class KimariteMatchesResponse(BaseModel):
    limit: int
    skip: int
    total: int
    records: list[Match] | None = []


class RikishiResponse(BaseModel):
    limit: int
    skip: int
    total: int
    records: list[Rikishi] | None = []


class RikishiMatchesResponse(BaseModel):
    limit: int
    skip: int
    total: int
    records: list[RikishiMatch] | None = []
