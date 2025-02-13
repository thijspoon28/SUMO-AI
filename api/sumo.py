from pydantic import BaseModel
import requests

from api.schemas import BashoBanzuke, BashoData, BashoTorikumi, KimariteMatches, Kimarites, Rikishi, RikishiMatches, RikishiStats, RikishiVersus, Rikishis


class SumoAPI:
    BASE_URL = "https://www.sumo-api.com"

    def request(cls, url: str, schema: BaseModel) -> BaseModel:
        response = requests.get(url)

        try:
            data = response.json()
        except Exception as exc:
            raise Exception("API IS PROBABLY DOWN") from exc
        
        # print(data["records"][0])
        result = schema(**data)

        return result
    
    def get_rikishis(cls) -> Rikishis:
        url = f"{cls.BASE_URL}/api/rikishis"

        return cls.request(url, Rikishis)
    
    def get_rikishi(cls, rikishi_id) -> Rikishi:
        url = f"{cls.BASE_URL}/api/rikishi/{rikishi_id}"

        return cls.request(url, Rikishi)
    
    def get_rikishi_stats(cls, rikishi_id) -> RikishiStats:
        url = f"{cls.BASE_URL}/api/rikishi/{rikishi_id}/stats"

        return cls.request(url, RikishiStats)
    
    def get_rikishi_matches(cls, rikishi_id) -> RikishiMatches:
        url = f"{cls.BASE_URL}/api/rikishi/{rikishi_id}/matches"
        
        return cls.request(url, RikishiMatches)
    
    def get_rikishi_versus(cls, rikishi_id, opponent_id) -> RikishiVersus:
        url = f"{cls.BASE_URL}/api/rikishi/{rikishi_id}/matches/{opponent_id}"
        
        return cls.request(url, RikishiVersus)
    
    def get_basho(cls, basho_id) -> BashoData:
        url = f"{cls.BASE_URL}/api/basho/{basho_id}"
        
        return cls.request(url, BashoData)
    
    def get_basho_banzuke(cls, basho_id, division) -> BashoBanzuke:
        """
        Division : Makuuchi, Juryo, Makushita, Sandanme, Jonidan, or Jonokuchi
        """
        url = f"{cls.BASE_URL}/api/basho/{basho_id}/banzuke/{division}"
        
        return cls.request(url, BashoBanzuke)
    
    def get_basho_torikumi(cls, basho_id, division, day) -> BashoTorikumi:
        url = f"{cls.BASE_URL}/api/basho/{basho_id}/torikumi/{division}/{day}"
        
        return cls.request(url, BashoTorikumi)
    
    def get_kimarite(cls, sortField: str = "count") -> Kimarites:
        """
        sortField : count, kimarite, lastUsage
        """

        url = f"{cls.BASE_URL}/api/kimarite?sortField={sortField}"
        
        return cls.request(url, Kimarites)
    
    def get_kimarite_detail(cls, kimarite) -> KimariteMatches:
        url = f"{cls.BASE_URL}/api/kimarite/{kimarite}"
        
        return cls.request(url, KimariteMatches)
    
    # def get_measurements(cls):
    #     url = f"{cls.BASE_URL}/api/measurements"
        
    #     return cls.request(url, Measurements)
    
    # def get_ranks(cls):
    #     url = f"{cls.BASE_URL}/api/ranks"
        
    #     return cls.request(url, Ranks)
    
    # def get_shikonas(cls):
    #     url = f"{cls.BASE_URL}/api/shikonas"
        
    #     return cls.request(url, Shikonas)
