from pydantic import BaseModel
import requests

from api.enums import Division, SortFields
from api.schemas import (
    BashoBanzuke,
    BashoData,
    BashoTorikumi,
    KimariteMatchesResponse,
    KimariteResponse,
    Measurement,
    Rank, 
    Rikishi,
    RikishiMatchesResponse,
    RikishiStats,
    RikishiVersus,
    RikishiResponse,
    Shikona,
)


class SumoAPI:
    BASE_URL = "https://www.sumo-api.com"

    def request(
        cls,
        url: str,
        *,
        params: dict | None = None,
        schema: BaseModel | None = None,
    ) -> BaseModel | dict:
        response = requests.get(url, params=params)

        try:
            data = response.json()
        except Exception as exc:
            raise Exception("API SOILED ITSELF (it's probably down)") from exc

        if schema:
            result = schema(**data)

            return result

        else:
            return data

    def get_rikishis(
        cls,
        shikonaEn: str | None = None,
        heya: str | None = None,
        sumodbId: int | None = None,
        nskId: int | None = None,
        intai: bool | None = None,
        measurements: bool | None = None,
        ranks: bool | None = None,
        shikonas: bool | None = None,
        limit: int | None = None,
        skip: int | None = None,
    ) -> RikishiResponse:
        """Returns a subset of rikishi in the database, hard limit of 1000, use limit & skip to access all records

        Args:
            shikonaEn (str, optional): search for a rikishi by English shikona. Defaults to None.
            heya (str, optional): search by heya, full name in English, e.g. Isegahama. Defaults to None.
            sumodbId (int, optional): search by sumoDB ID, e.g. 11927 = Terunofuji. Defaults to None.
            nskId (int, optional): search by official NSK ID, e.g. 3321 = Terunofuji. Defaults to None.
            intai (bool, optional): (retirement date) if missing, only active rikishi are searched. If true, retired rikishi are also searched. Defaults to None.
            measurements (bool, optional): if true, the changes in a rikishi's measurements over time will be included in the response. Defaults to None.
            ranks (bool, optional): if true, the changes in a rikishi's ranks over time will be included in the response. Defaults to None.
            shikonas (bool, optional): if true, the changes in a rikishi's shikonas over time will be included in the response. Defaults to None.
            limit (int, optional): how many results to return, 1000 hard limit. Defaults to None.
            skip (int, optional): skip over the number of results specified. Defaults to None.

        Returns:
            Rikishis:
        """

        url = f"{cls.BASE_URL}/api/rikishis"
        params = {}

        if shikonaEn:
            params["shikonaEn"] = shikonaEn
        if heya:
            params["heya"] = heya
        if sumodbId:
            params["sumodbId"] = sumodbId
        if nskId:
            params["nskId"] = nskId
        if intai is not None:
            params["intai"] = str(intai).lower()
        if measurements is not None:
            params["measurements"] = str(measurements).lower()
        if ranks is not None:
            params["ranks"] = str(ranks).lower()
        if shikonas is not None:
            params["shikonas"] = str(shikonas).lower()
        if limit:
            params["limit"] = min(limit, 1000)
        if skip:
            params["skip"] = skip

        return cls.request(url, params=params, schema=RikishiResponse)

    def get_rikishi(
        cls,
        rikishi_id: int,
        measurements: bool = None,
        ranks: bool = None,
        shikonas: bool = None,
    ) -> Rikishi:
        """Returns a single rikishi by id

        Args:
            rikishi_id (int): the rikishi id
            measurements (bool, optional): if true, the changes in a rikishi's measurements over time will be included in the response. Defaults to None.
            ranks (bool, optional): if true, the changes in a rikishi's ranks over time will be included in the response. Defaults to None.
            shikonas (bool, optional): if true, the changes in a rikishi's shikonas over time will be included in the response. Defaults to None.

        Returns:
            Rikishi:
        """
        url = f"{cls.BASE_URL}/api/rikishi/{rikishi_id}"
        params = {}

        if measurements is not None:
            params["measurements"] = str(measurements).lower()
        if ranks is not None:
            params["ranks"] = str(ranks).lower()
        if shikonas is not None:
            params["shikonas"] = str(shikonas).lower()

        return cls.request(url, params=params, schema=Rikishi)

    def get_rikishi_stats(cls, rikishi_id: int) -> RikishiStats:
        """Returns a single rikishi's overall performance stats, more data to be added later.

        Args:
            rikishi_id (int): the rikishi id

        Returns:
            RikishiStats:
        """
        url = f"{cls.BASE_URL}/api/rikishi/{rikishi_id}/stats"

        return cls.request(url, schema=RikishiStats)

    def get_rikishi_matches(
        cls,
        rikishi_id: int,
        basho_id: str | None = None,
    ) -> RikishiMatchesResponse:
        """Returns all matches of a rikishi. Sorted by basho, then by day, most to least recent.

        Args:
            bashoId (str): filters the matches by a specific basho YYYYMM e.g. 202303

        Returns:
            RikishiStats:
        """
        url = f"{cls.BASE_URL}/api/rikishi/{rikishi_id}/matches"
        params = {}

        if basho_id is not None:
            params["bashoId"] = basho_id

        return cls.request(url, params=params, schema=RikishiMatchesResponse)

    def get_rikishi_versus(
        cls,
        rikishi_id: int,
        opponent_id: int,
        basho_id: str | None = None,
    ) -> RikishiVersus:
        """Returns all matches between two rikishi. Sorted by basho, then by day, most to least recent.

        Args:
            rikishi_id (int): the rikishi id
            opponent_id (int): the opponent id
            basho_id (str): filters the matches by a specific basho YYYYMM e.g. 202303

        Returns:
            RikishiVersus:
        """
        url = f"{cls.BASE_URL}/api/rikishi/{rikishi_id}/matches/{opponent_id}"
        params = {}

        if basho_id is not None:
            params["bashoId"] = basho_id

        return cls.request(url, params=params, schema=RikishiVersus)

    def get_basho(
        cls,
        basho_id: str,
    ) -> BashoData:
        """Returns a single basho, where bashoId is in the format YYYYMM, with the yusho and sansho details for the basho.

        Args:
            basho_id (str): the basho id, is in the format YYYYMM

        Returns:
            BashoData:
        """
        url = f"{cls.BASE_URL}/api/basho/{basho_id}"

        return cls.request(url, schema=BashoData)

    def get_basho_banzuke(
        cls,
        basho_id: str,
        division: Division | str,
    ) -> BashoBanzuke:
        """Returns a single basho, where bashoId is in the format YYYYMM, and the specified division's banzuke,
        where the division is any of Makuuchi, Juryo, Makushita, Sandanme, Jonidan or Jonokuchi.

        Args:
            basho_id (str): the basho id, is in the format YYYYMM
            division (Division): the division [Makuuchi, Juryo, Makushita, Sandanme, Jonidan or Jonokuchi]

        Returns:
            BashoBanzuke:
        """
        division_value = division if isinstance(division, str) else division.value

        url = f"{cls.BASE_URL}/api/basho/{basho_id}/banzuke/{division_value}"

        return cls.request(url, schema=BashoBanzuke)

    def get_basho_torikumi(
        cls,
        basho_id: str,
        division: Division | str,
        day: int,
    ) -> BashoTorikumi:
        """Returns a single basho, where bashoId is in the format YYYYMM, and the specified division's torikumi
        of a given day.

        Args:
            basho_id (str): the basho id, is in the format YYYYMM
            division (Division): the division [Makuuchi, Juryo, Makushita, Sandanme, Jonidan or Jonokuchi]
            day (int): 1 to 15 (or up to the number of playoff matches)

        Returns:
            BashoTorikumi:
        """
        division_value = division if isinstance(division, str) else division.value

        url = f"{cls.BASE_URL}/api/basho/{basho_id}/torikumi/{division_value}/{day}"

        return cls.request(url, schema=BashoTorikumi)

    def get_kimarite(
        cls,
        sortField: SortFields = SortFields.count,
        ascending: bool = True,
        limit: int | None = None,
        skip: int | None = None,
    ) -> KimariteResponse:
        """Returns statistics on the usage of kimarite including the count of usage and the last basho and day used.
        NOTE: the lastUsage is not gauranteed to be the actual last use on the specified day of the basho

        Args:
            sortField (str, optional): choose a field to sort by. Defaults to "count".
            ascending (bool, optional): asc | desc. Defaults to True.
            limit (int, optional): how many results to return, 1000 hard limit. Defaults to None.
            skip (int, optional): skip over the number of results specified. Defaults to None.

        Returns:
            Kimarites:
        """

        url = f"{cls.BASE_URL}/api/kimarite"
        params = {}

        params["sortField"] = sortField
        params["sortOrder"] = "asc" if ascending else "desc"

        if limit:
            params["limit"] = min(limit, 1000)
        if skip:
            params["skip"] = skip

        return cls.request(url, params=params, schema=KimariteResponse)

    def get_kimarite_detail(
        cls,
        kimarite: str,
        ascending: bool = True,
        limit: int | None = None,
        skip: int | None = None,
    ) -> KimariteMatchesResponse:
        """Returns matches where the specified kimarite was used
        NOTE: the sort order is by basho then day and is not guaranteed to be the actual use order on that day.

        Args:
            kimarite (str): the kimarite
            ascending (bool, optional): asc | desc. Defaults to True.
            limit (int, optional): how many results to return, 1000 hard limit. Defaults to None.
            skip (int, optional): skip over the number of results specified. Defaults to None.

        Returns:
            KimariteMatches:
        """
        url = f"{cls.BASE_URL}/api/kimarite/{kimarite}"
        params = {}

        params["sortOrder"] = "asc" if ascending else "desc"

        if limit:
            params["limit"] = min(limit, 1000)
        if skip:
            params["skip"] = skip

        return cls.request(url, schema=KimariteMatchesResponse)

    def get_measurements(
        cls,
        rikishi_id: int | None = None,
        basho_id: str | None = None,
        ascending: bool = True,
    ) -> list[Measurement]:
        """Returns measurement changes by rikishi or basho
        NOTE: the sort order is by basho, default descending order.

        Args:
            rikishi_id (int, optional): filter on rikishi by ID. Defaults to None.
            basho_id (str, optional): filter on basho in format (format yyyymm, e.g 202301). Defaults to None.
            ascending (bool, optional): asc | desc. Defaults to True.

        Returns:
            list[Measurement]:
        """
        url = f"{cls.BASE_URL}/api/measurements"
        params = {}

        params["sortOrder"] = "asc" if ascending else "desc"

        if rikishi_id:
            params["rikishiId"] = rikishi_id
        if basho_id:
            params["bashoId"] = basho_id

        data = cls.request(url, params=params)
        return [Measurement(**d) for d in data]

    def get_ranks(
        cls,
        rikishi_id: int | None = None,
        basho_id: str | None = None,
        # ascending: bool = True,
    ) -> list[Rank]:
        """Returns rank changes by rikishi or basho
        NOTE: the sort order is by basho, default descending order.

        Args:
            rikishi_id (int, optional): filter on rikishi by ID. Defaults to None.
            basho_id (str, optional): filter on basho in format (format yyyymm, e.g 202301). Defaults to None.
            ascending (bool, optional): asc | desc. Defaults to True.

        Returns:
            list[Rank]:
        """
        url = f"{cls.BASE_URL}/api/ranks"
        params = {}

        # params["sortOrder"] = "asc" if ascending else "desc"

        if rikishi_id:
            params["rikishiId"] = rikishi_id
        if basho_id:
            params["bashoId"] = basho_id

        if not rikishi_id and not basho_id:
            raise ValueError("Provide 'rikishi_id', 'basho_id' or both")

        data = cls.request(url, params=params)
        return [Rank(**d) for d in data]

    def get_shikonas(
        cls,
        rikishi_id: int | None = None,
        basho_id: str | None = None,
        # ascending: bool = True,
    ) -> list[Shikona]:
        """Returns shikona changes by rikishi or basho
        NOTE: the sort order is by basho, default descending order.

        Args:
            rikishi_id (int, optional): filter on rikishi by ID. Defaults to None.
            basho_id (str, optional): filter on basho in format (format yyyymm, e.g 202301). Defaults to None.
            ascending (bool, optional): asc | desc. Defaults to True.

        Returns:
            list[Shikona]:
        """
        url = f"{cls.BASE_URL}/api/shikonas"
        params = {}

        # params["sortOrder"] = "asc" if ascending else "desc"

        if rikishi_id:
            params["rikishiId"] = rikishi_id
        if basho_id:
            params["bashoId"] = basho_id

        data = cls.request(url, params=params)
        return [Shikona(**d) for d in data]
