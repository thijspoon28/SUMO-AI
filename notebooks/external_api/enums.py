import enum


class Division(str, enum.Enum):
    Makuuchi = "Makuuchi"
    Juryo = "Juryo"
    Makushita = "Makushita"
    Sandanme = "Sandanme"
    Jonidan = "Jonidan"
    Jonokuchi = "Jonokuchi"


class SortFields(str, enum.Enum):
    count = "count"  # type: ignore
    kimarite = "kimarite"
    lastUsage = "lastUsage"
