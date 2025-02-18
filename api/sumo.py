from typing import Any, Type, TypeVar, get_args, get_origin, overload
from pydantic import BaseModel
import requests  # type: ignore

from api.enums import Division, SortFields
from api.response_schemas import BaseResponse, BashoBanzukeResponse, BashoResponse, BashoTorikumiResponse, KimariteMatchesResponse, KimariteResponse, MeasurementResponse, RankResponse, RikishiMatchesResponse, RikishiResponse, RikishiStatsResponse, RikishiVersusResponse, RikishisResponse, ShikonaResponse


T = TypeVar("T", bound=BaseResponse)


class SumoAPI:
    BASE_URL = "https://www.sumo-api.com"

    @overload
    @classmethod
    def request(
        cls,
        url: str,
        *,
        schema: Type[T],
        params: dict | None = None
    ) -> T: ...

    @overload
    @classmethod
    def request(
        cls,
        url: str,
        *,
        schema: None = None,
        params: dict | None = None
    ) -> dict: ...

    @classmethod
    def request(
        cls,
        url: str,
        *,
        schema: Type[T] | None = None,
        params: dict | None = None,
    ) -> T | dict:
        if not params:
            params = {}

        if params.get("skip") is None:
            params["skip"] = 0
        if params.get("limit") is None:
            params["limit"] = 1000

        response = requests.get(url, params=params)

        try:
            data = response.json()
        except Exception as exc:
            print()
            print(url, params)
            print(response)
            print(response.text)
            raise Exception("API SOILED ITSELF (it's probably down)") from exc

        if not schema:
            return data
        
        result = schema(
            skip=params["skip"],
            limit=params["limit"],
            total=data.get("total") if isinstance(data, dict) else None,
        )
        if isinstance(data, dict) and (records := data.get("records")) is not None:
            if isinstance(records, list) and len(records) > 0:
                # Dynamically get the type of records
                record_type = schema.__annotations__["records"].__args__[0]
                result.records = [record_type(**r) for r in records]
            else:
                result.records = []
        
        elif isinstance(data, list):
            # Dynamically parse list of data as records
            record_type = schema.__annotations__["records"]
            record_type = next(t for t in get_args(record_type) if t is not type(None))

            # if get_origin(record_type) is Union:
            #     record_type = next(t for t in get_args(record_type) if t is not type(None))

            if get_origin(record_type) is list:
                record_type = get_args(record_type)[0]
                
            print(record_type, schema.__annotations__["records"])
            result.records = [record_type(**item) for item in data]
        
        else:
            record_type = schema.__annotations__["record"].__args__[0]
            if isinstance(record_type, type) and issubclass(record_type, BaseModel):
                result.record = record_type(**data)

        return result

    def scrape(cls, url: str, params: dict, schema: Type[T]) -> T:
        if params.get("skip") is None:
            params["skip"] = 0
        if params.get("limit") is None:
            params["limit"] = 1000

        result = None

        while True:
            data = cls.request(url, params=params, schema=schema)
            amount = len(data.records) if data.records is not None else 0  # type: ignore

            if amount == 0:
                break

            params["skip"] += amount

            if result is not None:
                result.records += data.records  # type: ignore

            else:
                result = data
        
        if result is None:
            raise Exception("Ahw shit")
        
        return result

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
        scrape: bool = False,
    ) -> RikishisResponse:
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
        params: dict[str, Any] = {}
        
        params["intai"] = True

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

        if scrape:
            return cls.scrape(url, params=params, schema=RikishisResponse)

        return cls.request(url, params=params, schema=RikishisResponse)

    def get_rikishi(
        cls,
        rikishi_id: int,
        measurements: bool | None = None,
        ranks: bool | None = None,
        shikonas: bool | None = None,
    ) -> RikishiResponse:
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
        params: dict[str, Any] = {}
        
        params["intai"] = True

        if measurements is not None:
            params["measurements"] = str(measurements).lower()
        if ranks is not None:
            params["ranks"] = str(ranks).lower()
        if shikonas is not None:
            params["shikonas"] = str(shikonas).lower()

        return cls.request(url, params=params, schema=RikishiResponse)

    def get_rikishi_stats(
        cls,
        rikishi_id: int,
    ) -> RikishiStatsResponse:
        """Returns a single rikishi's overall performance stats, more data to be added later.

        Args:
            rikishi_id (int): the rikishi id

        Returns:
            RikishiStats:
        """
        url = f"{cls.BASE_URL}/api/rikishi/{rikishi_id}/stats"

        return cls.request(url, schema=RikishiStatsResponse)

    def get_rikishi_matches(
        cls,
        rikishi_id: int,
        basho_id: str | None = None,
        limit: int | None = None,
        skip: int | None = None,
        scrape: bool = False,
    ) -> RikishiMatchesResponse:
        """Returns all matches of a rikishi. Sorted by basho, then by day, most to least recent.

        Args:
            bashoId (str): filters the matches by a specific basho YYYYMM e.g. 202303

        Returns:
            RikishiStats:
        """
        url = f"{cls.BASE_URL}/api/rikishi/{rikishi_id}/matches"
        params: dict[str, Any] = {}

        if basho_id is not None:
            params["bashoId"] = basho_id
        if limit:
            params["limit"] = min(limit, 1000)
        if skip:
            params["skip"] = skip

        if scrape:
            return cls.scrape(url, params=params, schema=RikishiMatchesResponse)

        return cls.request(url, params=params, schema=RikishiMatchesResponse)

    def get_rikishi_versus(
        cls,
        rikishi_id: int,
        opponent_id: int,
        basho_id: str | None = None,
        limit: int | None = None,
        skip: int | None = None,
        scrape: bool = False,
    ) -> RikishiVersusResponse:
        """Returns all matches between two rikishi. Sorted by basho, then by day, most to least recent.

        Args:
            rikishi_id (int): the rikishi id
            opponent_id (int): the opponent id
            basho_id (str): filters the matches by a specific basho YYYYMM e.g. 202303

        Returns:
            RikishiVersus:
        """
        url = f"{cls.BASE_URL}/api/rikishi/{rikishi_id}/matches/{opponent_id}"
        params: dict[str, Any] = {}

        if basho_id is not None:
            params["bashoId"] = basho_id
        if limit:
            params["limit"] = min(limit, 1000)
        if skip:
            params["skip"] = skip

        if scrape:
            return cls.scrape(url, params=params, schema=RikishiVersusResponse)

        return cls.request(url, params=params, schema=RikishiVersusResponse)

    def get_basho(
        cls,
        basho_id: str,
    ) -> BashoResponse:
        """Returns a single basho, where bashoId is in the format YYYYMM, with the yusho and sansho details for the basho.

        Args:
            basho_id (str): the basho id, is in the format YYYYMM

        Returns:
            BashoData:
        """
        url = f"{cls.BASE_URL}/api/basho/{basho_id}"

        return cls.request(url, schema=BashoResponse)

    def get_basho_banzuke(
        cls,
        basho_id: str,
        division: Division | str,
        limit: int | None = None,
        skip: int | None = None,
        scrape: bool = False,
    ) -> BashoBanzukeResponse:
        """Returns a single basho, where bashoId is in the format YYYYMM, and the specified division's banzuke,
        where the division is any of Makuuchi, Juryo, Makushita, Sandanme, Jonidan or Jonokuchi.

        Args:
            basho_id (str): the basho id, is in the format YYYYMM
            division (Division): the division [Makuuchi, Juryo, Makushita, Sandanme, Jonidan or Jonokuchi]

        Returns:
            BashoBanzuke:
        """
        division_value = division.value if isinstance(division, Division) else division

        url = f"{cls.BASE_URL}/api/basho/{basho_id}/banzuke/{division_value}"
        params: dict[str, Any] = {}

        if limit:
            params["limit"] = min(limit, 1000)
        if skip:
            params["skip"] = skip

        if scrape:
            return cls.scrape(url, params=params, schema=BashoBanzukeResponse)

        return cls.request(url, schema=BashoBanzukeResponse)

    def get_basho_torikumi(
        cls,
        basho_id: str,
        division: Division | str,
        day: int,
        limit: int | None = None,
        skip: int | None = None,
        scrape: bool = False,
    ) -> BashoTorikumiResponse:
        """Returns a single basho, where bashoId is in the format YYYYMM, and the specified division's torikumi
        of a given day.

        Args:
            basho_id (str): the basho id, is in the format YYYYMM
            division (Division): the division [Makuuchi, Juryo, Makushita, Sandanme, Jonidan or Jonokuchi]
            day (int): 1 to 15 (or up to the number of playoff matches)

        Returns:
            BashoTorikumi:
        """
        division_value = division.value if isinstance(division, Division) else division

        url = f"{cls.BASE_URL}/api/basho/{basho_id}/torikumi/{division_value}/{day}"
        params: dict[str, Any] = {}

        if limit:
            params["limit"] = min(limit, 1000)
        if skip:
            params["skip"] = skip

        if scrape:
            return cls.scrape(url, params=params, schema=BashoTorikumiResponse)

        return cls.request(url, schema=BashoTorikumiResponse)

    def get_kimarite(
        cls,
        sortField: SortFields = SortFields.count,
        ascending: bool = True,
        limit: int | None = None,
        skip: int | None = None,
        scrape: bool = False,
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
        params: dict[str, Any] = {}

        params["sortField"] = sortField
        params["sortOrder"] = "asc" if ascending else "desc"

        if limit:
            params["limit"] = min(limit, 1000)
        if skip:
            params["skip"] = skip

        if scrape:
            return cls.scrape(url, params=params, schema=KimariteResponse)

        return cls.request(url, params=params, schema=KimariteResponse)

    def get_kimarite_detail(
        cls,
        kimarite: str,
        ascending: bool = True,
        limit: int | None = None,
        skip: int | None = None,
        scrape: bool = False,
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
        params: dict[str, Any] = {}

        params["sortOrder"] = "asc" if ascending else "desc"

        if limit:
            params["limit"] = min(limit, 1000)
        if skip:
            params["skip"] = skip

        if scrape:
            return cls.scrape(url, params=params, schema=KimariteMatchesResponse)

        return cls.request(url, params=params, schema=KimariteMatchesResponse)

    def get_measurements(
        cls,
        rikishi_id: int | None = None,
        basho_id: str | None = None,
        # ascending: bool = True,
        limit: int | None = None,
        skip: int | None = None,
        scrape: bool = False,
    ) -> MeasurementResponse:
        """Returns measurement changes by rikishi or basho
        NOTE: the sort order is by basho, default descending order.

        Args:
            rikishi_id (int, optional): filter on rikishi by ID. Defaults to None.
            basho_id (str, optional): filter on basho in format (format yyyymm, e.g 202301). Defaults to None.
            ascending (bool, optional): asc | desc. Defaults to True.
            limit (int, optional): how many results to return, 1000 hard limit. Defaults to None.
            skip (int, optional): skip over the number of results specified. Defaults to None.

        Returns:
            list[Measurement]:
        """
        url = f"{cls.BASE_URL}/api/measurements"
        params: dict[str, Any] = {}

        # params["sortOrder"] = "asc" if ascending else "desc"

        if rikishi_id:
            params["rikishiId"] = rikishi_id
        if basho_id:
            params["bashoId"] = basho_id
        if limit:
            params["limit"] = min(limit, 1000)
        if skip:
            params["skip"] = skip

        if scrape:
            return cls.scrape(url, params=params, schema=MeasurementResponse)

        return cls.request(url, params=params, schema=MeasurementResponse)

    def get_ranks(
        cls,
        rikishi_id: int | None = None,
        basho_id: str | None = None,
        # ascending: bool = True,
        limit: int | None = None,
        skip: int | None = None,
        scrape: bool = False,
    ) -> RankResponse:
        """Returns rank changes by rikishi or basho
        NOTE: the sort order is by basho, default descending order.

        Args:
            rikishi_id (int, optional): filter on rikishi by ID. Defaults to None.
            basho_id (str, optional): filter on basho in format (format yyyymm, e.g 202301). Defaults to None.
            ascending (bool, optional): asc | desc. Defaults to True.
            limit (int, optional): how many results to return, 1000 hard limit. Defaults to None.
            skip (int, optional): skip over the number of results specified. Defaults to None.

        Returns:
            list[Rank]:
        """
        url = f"{cls.BASE_URL}/api/ranks"
        params: dict[str, Any] = {}

        # params["sortOrder"] = "asc" if ascending else "desc"

        if rikishi_id:
            params["rikishiId"] = rikishi_id
        if basho_id:
            params["bashoId"] = basho_id
        if limit:
            params["limit"] = min(limit, 1000)
        if skip:
            params["skip"] = skip

        if not rikishi_id and not basho_id:
            raise ValueError("Provide 'rikishi_id', 'basho_id' or both")

        if scrape:
            return cls.scrape(url, params=params, schema=RankResponse)

        return cls.request(url, params=params, schema=RankResponse)

    def get_shikonas(
        cls,
        rikishi_id: int | None = None,
        basho_id: str | None = None,
        # ascending: bool = True,
        limit: int | None = None,
        skip: int | None = None,
        scrape: bool = False,
    ) -> ShikonaResponse:
        """Returns shikona changes by rikishi or basho
        NOTE: the sort order is by basho, default descending order.

        Args:
            rikishi_id (int, optional): filter on rikishi by ID. Defaults to None.
            basho_id (str, optional): filter on basho in format (format yyyymm, e.g 202301). Defaults to None.
            ascending (bool, optional): asc | desc. Defaults to True.
            limit (int, optional): how many results to return, 1000 hard limit. Defaults to None.
            skip (int, optional): skip over the number of results specified. Defaults to None.

        Returns:
            list[Shikona]:
        """
        url = f"{cls.BASE_URL}/api/shikonas"
        params: dict[str, Any] = {}

        # params["sortOrder"] = "asc" if ascending else "desc"

        if rikishi_id:
            params["rikishiId"] = rikishi_id
        if basho_id:
            params["bashoId"] = basho_id
        if limit:
            params["limit"] = min(limit, 1000)
        if skip:
            params["skip"] = skip

        if scrape:
            return cls.scrape(url, params=params, schema=ShikonaResponse)

        return cls.request(url, params=params, schema=ShikonaResponse)
