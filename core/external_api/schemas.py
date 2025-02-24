from datetime import datetime
from pydantic import BaseModel, ConfigDict


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
    shikonaEn: str
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
    nskId: int | None = None
    shikonaEn: str | None = None
    shikonaJp: str | None = None
    currentRank: str | None = None
    heya: str | None = None
    birthDate: datetime | None = None
    shusshin: str | None = None
    measurementHistory: list[Measurement] | None = []
    rankHistory: list[Rank] | None = []
    shikonaHistory: list[Shikona] | None = []
    height: float | None = None
    weight: float | None = None
    debut: str | None = None
    intai: datetime | None = None
    updatedAt: datetime | None = None
    createdAt: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class RikishiVersus(BaseModel):
    kimariteLosses: dict[str, int]
    kimariteWins: dict[str, int]
    matches: list[RikishiMatch] = []
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


class BashoTorikumi(BaseModel):
    date: str
    startDate: str
    endDate: str
    yusho: list[TorikumiYusho] | None = []
    specialPrizes: list[SpecialPrize] | None = []
    torikumi: list[Match] | None = []


class ValidateMeasurement(BaseModel):
    basho_id: str
    rikishi_id: int
    height: float
    weight: float

    model_config = ConfigDict(from_attributes=True)


class ValidateRank(BaseModel):
    basho_id: str
    rikishi_id: int
    rank_value: int
    rank: str
    
    model_config = ConfigDict(from_attributes=True)


class ValidateShikona(BaseModel):
    basho_id: str
    rikishi_id: int
    shikona_en: str
    shikona_jp: str | None = None
    
    model_config = ConfigDict(from_attributes=True)


class ValidateRikishi(BaseModel):
    id: int
    sumodb_id: int | None = None
    nsk_id: int
    shikona_en: str
    shikona_jp: str | None = None
    current_rank: str
    heya: str | None = None
    birth_date: datetime | None = None
    shusshin: str | None = None
    height: float
    weight: float
    debut: str
    intai: datetime | None = None
    updated_at: datetime | None = None
    created_at: datetime | None = None

    absence_by_division: dict[str, int]
    basho_count: int
    basho_count_by_division: dict[str, int]
    loss_by_division: dict[str, int]
    sansho: dict[str, int]
    total_absences: int
    total_by_division: dict[str, int]
    total_losses: int
    total_matches: int
    total_wins: int
    wins_by_division: dict[str, int]
    yusho_count: int
    yusho_count_by_division: dict[str, int]

    measurementHistory: list[ValidateMeasurement] | None = []
    rankHistory: list[ValidateRank] | None = []
    shikonaHistory: list[ValidateShikona] | None = []

    model_config = ConfigDict(from_attributes=True)

