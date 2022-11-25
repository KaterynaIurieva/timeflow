from fastapi import APIRouter, Depends
from ..utils import engine, get_session
from sqlmodel import Session, select
from ..models.epic import Epic
from ..models.client import Client
from ..models.sponsor import Sponsor
from ..models.team import Team
from sqlalchemy.exc import NoResultFound
from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel

router = APIRouter(prefix="/api/epics", tags=["epic"])


@router.post("/")
async def post_epic(
    *,
    epic: Epic,
    session: Session = Depends(get_session),
):
    """
    Post new epic.

    Parameters
    ----------
    epic : Epic
        Epic that is to be added to the database.
    session : Session
        SQL session that is to be used to add the epic.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement1 = select(Epic).where(Epic.name == epic.name)
    try:
        result = session.exec(statement1).one()
        return False
    except NoResultFound:
        session.add(epic)
        session.commit()
        session.refresh(epic)
        return epic


@router.get("/")
async def get_epics_list(
    session: Session = Depends(get_session),
    is_active: bool = None,
):
    """
    Get list of epics.

    Parameters
    ----------
    session : Session
        SQL session that is to be used to get a list of the epics.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = (
        select(
            Epic.id,
            Epic.short_name,
            Epic.name.label("epic_name"),
            Team.name.label("team_name"),
            Sponsor.name.label("sponsor_name"),
            Epic.start_date,
            Epic.is_active,
        )
        .select_from(Epic)
        .join(Team)
        .join(Sponsor)
    )
    if is_active != None:
        statement_final = (
            statement.order_by(Epic.is_active.desc())
            .order_by(Epic.start_date.desc())
            .order_by(Epic.name.asc())
        )
    else:
        statement_final = (
            statement.order_by(Epic.is_active.desc())
            .order_by(Epic.start_date.desc())
            .order_by(Epic.name.asc())
        )

    results = session.exec(statement_final).all()
    return results


@router.get("/teams/{team_id}/sponsors/{sponsor_id}/")
async def get_epic_by_team_sponsor(
    team_id: int, sponsor_id: int, session: Session = Depends(get_session)
):
    """
    Get list of epics by team id and sponsor id.

    Parameters
    ----------
    team_id : int
        ID of team to pull epics from.
    sponsor_id : int
        ID of sponsor to pull epics from.
    session : Session
        SQL session that is to be used to pull the epics.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = (
        select(
            Epic.id.label("epic_id"),
            Epic.name.label("epic_name"),
            Epic.start_date,
            Team.name.label("team_name"),
            Sponsor.short_name.label("sponsor_short_name"),
        )
        .select_from(Epic)
        .join(Team)
        .join(Sponsor)
        .where(Epic.team_id == team_id)
        .where(Epic.sponsor_id == sponsor_id)
        .where(Epic.is_active == True)
    )
    results = session.exec(statement).all()
    return results


@router.get("/{epic_id}/client-name")
async def get_client_name_by_epic_id(
    epic_id: int, session: Session = Depends(get_session)
):
    """
    Get client name from epic_id.

    Parameters
    ----------
    epic_id : int
        ID of epic to pull client name from.
    session : Session
        SQL session that is to be used to pull the client name.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = (
        select(Client.name.label("client_name"), Client.id.label("client_id"))
        .select_from(Epic)
        .join(Sponsor, isouter=True)
        .join(Client, isouter=True)
        .where(Epic.id == epic_id)
        .where(Client.is_active == True)
    )
    result = session.exec(statement).one()
    return result


@router.put("/{epic_id}/activate")
async def activate_epic(
    epic_id: str = None,
    session: Session = Depends(get_session),
):
    """
    Activate an epic using its ID as a key.

    Parameters
    ----------
    epic_id : str
        ID of epic to be activated.
    session : Session
        SQL session that is to be used to activate the epic.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Epic).where(Epic.id == epic_id)
    epic_to_activate = session.exec(statement).one()
    epic_to_activate.is_active = True
    epic_to_activate.updated_at = datetime.now()
    session.add(epic_to_activate)
    session.commit()
    session.refresh(epic_to_activate)
    return epic_to_activate


@router.put("/{epic_id}/deactivate")
async def deactivate_epic(
    epic_id: str = None,
    session: Session = Depends(get_session),
):
    """
    Deactivate an epic using its ID as a key.

    Parameters
    ----------
    epic_id : str
        ID of epic to be deactivated.
    session : Session
        SQL session that is to be used to deactivate the epic.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Epic).where(Epic.id == epic_id)
    epic_to_deactivate = session.exec(statement).one()
    epic_to_deactivate.is_active = False
    epic_to_deactivate.updated_at = datetime.now()
    session.add(epic_to_deactivate)
    session.commit()
    session.refresh(epic_to_deactivate)
    return epic_to_deactivate


@router.put("/{epic_id}/")
async def update_epic(
    epic_id: int,
    new_epic_name: Optional[str] = None,
    new_short_name: Optional[str] = None,
    new_team_id: Optional[int] = None,
    new_sponsor_id: Optional[int] = None,
    new_start_date: Optional[date] = None,
    session: Session = Depends(get_session),
    is_active: Optional[bool] = None,
):

    statement = select(Epic).where(Epic.id == epic_id)

    epic_to_update = session.exec(statement).one()

    if is_active != None:
        epic_to_update.is_active = is_active
    if new_epic_name != None:
        epic_to_update.name = new_epic_name
    if new_short_name != None:
        epic_to_update.short_name = new_short_name
    if new_team_id != None:
        epic_to_update.team_id = new_team_id
    if new_sponsor_id != None:
        epic_to_update.sponsor_id = new_sponsor_id
    if new_start_date != None:
        epic_to_update.start_date = new_start_date
    epic_to_update.updated_at = datetime.now()
    session.add(epic_to_update)
    session.commit()
    session.refresh(epic_to_update)
    return epic_to_update


class UpdateEpic(BaseModel):
    id: int
    epic_name: str
    short_name: str
    team_name: str
    sponsor_name: str
    start_date: date
    is_active: bool


@router.post("/bulk_update")
async def update_epics(
    epics: List[UpdateEpic],
    session: Session = Depends(get_session),
):
    for epic in epics:
        statement = select(Epic).where(Epic.id == epic.id)
        epic_to_update = session.exec(statement).one()

        statement2 = select(Team.id).where(Team.name == epic.team_name)
        team_id_to_update = session.exec(statement2).one()

        statement3 = select(Sponsor.id).where(Sponsor.name == epic.sponsor_name)
        sponsor_id_to_update = session.exec(statement3).one()

        epic_to_update.name = epic.epic_name
        epic_to_update.short_name = epic.short_name
        epic_to_update.team_id = team_id_to_update
        epic_to_update.sponsor_id = sponsor_id_to_update
        epic_to_update.start_date = epic.start_date
        epic_to_update.is_active = epic.is_active
        epic_to_update.updated_at = datetime.now()
    session.commit()
