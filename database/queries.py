from sqlalchemy import or_, select, text
from sqlalchemy.orm import aliased
from database.models import Basho, Match, Rikishi, RikishiBasho
from database.session import get_session
import pandas as pd


class Repo:
    def find_rikishi(rikishi_id: int) -> Basho | None:
        session = get_session()

        query = select(Rikishi).where(Rikishi.id == rikishi_id)

        result = session.execute(query).scalars().first()
        session.close()
        return result

    def find_basho(basho_id: str) -> Basho | None:
        session = get_session()

        query = select(Basho).where(Basho.id == basho_id)

        result = session.execute(query).scalars().first()
        session.close()
        return result

    def find_match(
        basho_id: str,
        division: str,
        id_one: int,
        id_two: int,
    ) -> Match | None:
        session = get_session()

        query = select(Match).where(
            Match.basho_id == basho_id,
            Match.division == division,
            or_(
                (Match.east_id == id_one) & (Match.west_id == id_two),
                (Match.east_id == id_two) & (Match.west_id == id_one),
            ),
        )
        result = session.execute(query).scalars().first()
        session.close()
        return result

class DfQueries:
    def basho_matches() -> pd.DataFrame:
        session = get_session()
        
        east_rikishi = aliased(Rikishi)
        west_rikishi = aliased(Rikishi)

        query = (
            session.query(
                Basho.id.label("basho_id"),
                # Basho.date.label("basho_date"),
                # Basho.start_date,
                # Basho.end_date,

                Match.day,
                Match.match_no,
                Match.division,
                Match.kimarite,

                Match.east_id.label("east_rikishi_id"),
                Match.east_shikona,
                Match.east_rank,
                east_rikishi.weight.label("east_weight"),
                east_rikishi.height.label("east_height"),

                Match.west_id.label("west_rikishi_id"),
                Match.west_shikona,
                Match.west_rank,
                west_rikishi.weight.label("west_weight"),
                west_rikishi.height.label("west_height"),

                Match.winner_id,
                Match.winner_en,
                Match.winner_jp,
            )
            .join(Match, Match.basho_id == Basho.id)
            .join(east_rikishi, east_rikishi.id == Match.east_id)
            .join(west_rikishi, west_rikishi.id == Match.west_id)
        )

        compiled_query = query.statement.compile(
            dialect=session.bind.dialect,  
            compile_kwargs={"literal_binds": True}  
        )

        df = pd.read_sql(text(str(compiled_query)), session.bind)

        session.close()
        return df
    
    def basho_rikishi() -> pd.DataFrame:
        session = get_session()

        query = (
            session.query(
                Basho.id.label("basho_id"),
                # Basho.date.label("basho_date"),
                # Basho.start_date,
                # Basho.end_date,

                RikishiBasho.rikishi_id,
                Rikishi.shikona_en.label("rikishi_shikona"),
                Rikishi.height.label("rikishi_height"),
                Rikishi.weight.label("rikishi_weight"),

                RikishiBasho.special_prize,
                RikishiBasho.yusho
            )
            .join(RikishiBasho, RikishiBasho.basho_id == Basho.id)
            .join(Rikishi, Rikishi.id == RikishiBasho.rikishi_id)
        )

        compiled_query = query.statement.compile(
            dialect=session.bind.dialect,  
            compile_kwargs={"literal_binds": True}  
        )

        df = pd.read_sql(text(str(compiled_query)), session.bind)

        session.close()
        return df

