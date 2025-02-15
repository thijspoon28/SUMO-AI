from sqlalchemy import or_, select
from api.schemas import Rikishi
from database.models import Basho, Match
from database.session import get_session



def find_rikishi(rikishi_id: int) -> Basho | None:
    session = get_session()

    query = select(Rikishi).where(
        Rikishi.id == rikishi_id
    )

    return session.execute(query).scalars().first()


def find_basho(basho_id: str) -> Basho | None:
    session = get_session()

    query = select(Basho).where(
        Basho.id == basho_id
    )

    return session.execute(query).scalars().first()


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

    return session.execute(query).scalars().first()
