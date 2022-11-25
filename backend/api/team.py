from fastapi import APIRouter, Depends
from ..utils import engine, get_session
from sqlmodel import Session, select, or_
from ..models.team import Team
from ..models.user import AppUser
from sqlalchemy.exc import NoResultFound
from datetime import datetime
from typing import List
from pydantic import BaseModel

router = APIRouter(prefix="/api/teams", tags=["team"])


@router.post("/")
async def post_team(
    *,
    team: Team,
    session: Session = Depends(get_session),
):
    """
    Post new team.

    Parameters
    ----------
    team : Team
        Team that is to be added to the database.
    session : Session
        SQL session that is to be used to add the team.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Team).where(or_(Team.name == team.name, Team.id == team.id))
    try:
        result = session.exec(statement).one()
        return False
    except NoResultFound:
        session.add(team)
        session.commit()
        session.refresh(team)
        return team


@router.get("/")
async def get_teams_list(
    session: Session = Depends(get_session), is_active: bool = None
):
    """
    Get list of all teams.

    Parameters
    ----------
    session : Session
        SQL session that is to be used to get the list of teams.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = (
        select(
            Team.id,
            Team.name.label("name"),
            Team.short_name.label("short_name"),
            # Team.lead_user_id,
            # Team.is_active,
            # AppUser.id,
            # AppUser.username.label("username"),
            # AppUser.first_name,
            # AppUser.last_name,
            (AppUser.first_name + " " + AppUser.last_name).label("full_lead_name"),
            Team.is_active,
        )
        .join(AppUser)
        .where(AppUser.id == Team.lead_user_id)
    )
    if is_active != None:
        statement_final = statement.order_by(Team.is_active.desc()).order_by(
            Team.name.asc()
        )
    else:
        statement_final = statement.order_by(Team.is_active.desc()).order_by(
            Team.name.asc()
        )

    results = session.exec(statement_final).all()
    return results


@router.get("/active")
async def get_active_team_list(session: Session = Depends(get_session)):
    """
    Get list of active teams.

    Parameters
    ----------
    session : Session
        SQL session that is to be used to get a list of the active teams.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = (
        select(
            Team.id,
            Team.lead_user_id,
            Team.name.label("name"),
            Team.short_name.label("short_name"),
            AppUser.id,
            AppUser.username.label("username"),
        )
        .join(AppUser)
        .where(Team.is_active == True)
    )
    results = session.exec(statement).all()
    return results


@router.get("/{name}")
async def read_teams(name: str = None, session: Session = Depends(get_session)):
    """
    Read the contents of a given team.

    Parameters
    ----------
    team_name : str
        Name of team to be read.
    session : Session
        SQL session that is to be used to read the team.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Team).where(Team.name == name)
    try:
        result = session.exec(statement).one()
        return result
    except NoResultFound:
        msg = f"""There is no team named {name}"""
        return msg


@router.get("/{team_id}/user-name")
async def get_username_by_team_id(
    team_id: int, session: Session = Depends(get_session)
):
    """
    Get user name by team id.

    Parameters
    ----------
    team_id : str
        ID of team to pull user name from.
    session : Session
        SQL session that is to be used to get the user name.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = (
        select(Team.id, AppUser.id, AppUser.name)
        .join(AppUser)
        .where(Team.id == team_id)
        .where(AppUser.active == True)
    )
    result = session.exec(statement).one()
    return result


@router.put("/{name}/activate")
async def activate_team(
    name: str = None,
    session: Session = Depends(get_session),
):
    """
    Activate a team.

    Parameters
    ----------
    team_name : str
        Name of team to be activated.
    session : Session
        SQL session that is to be used to activate the team.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Team).where(Team.name == name)
    team_to_activate = session.exec(statement).one()
    team_to_activate.is_active = True
    team_to_activate.updated_at = datetime.now()
    session.add(team_to_activate)
    session.commit()
    session.refresh(team_to_activate)
    return team_to_activate


@router.put("/{name}/deactivate")
async def deactivate_team(
    team_name: str = None,
    session: Session = Depends(get_session),
):
    """
    Deactivate a team.

    Parameters
    ----------
    team_name : str
        Name of team to be deactivated.
    session : Session
        SQL session that is to be used to deactivate the team.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Team).where(Team.name == team_name)
    team_to_deactivate = session.exec(statement).one()
    team_to_deactivate.is_active = False
    team_to_deactivate.updated_at = datetime.now()
    session.add(team_to_deactivate)
    session.commit()
    session.refresh(team_to_deactivate)
    return team_to_deactivate


@router.put("/{team_id}/")
async def update_team(
    team_id: int = None,
    new_lead_user_id: str = None,
    new_name: str = None,
    is_active: bool = None,
    session: Session = Depends(get_session),
):
    """
    Update a team with new values.

    Parameters
    ----------
    id : str
        ID of team to be updated.
    lead_user_id : str
        Updated lead user ID.
    name : str
        Updated name of team.
    is_active : bool
        Updated status of team.
    session : Session
        SQL session that is to be used to update the team.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Team).where(Team.id == team_id)
    team_to_update = session.exec(statement).one()
    if new_lead_user_id != None:
        team_to_update.lead_user_id = new_lead_user_id
    if new_name != None:
        team_to_update.name = new_name
    if is_active != None:
        team_to_update.is_active = is_active
    session.add(team_to_update)
    team_to_update.updated_at = datetime.now()
    session.commit()
    session.refresh(team_to_update)
    return True


class UpdateTeam(BaseModel):
    id: int
    name: str
    short_name: str
    full_lead_name: str
    is_active: bool


@router.post("/bulk_update")
async def update_team(
    teams: List[UpdateTeam],
    session: Session = Depends(get_session),
):
    for team in teams:
        print("team", team)
        statement = select(Team).where(Team.id == team.id)
        team_to_update = session.exec(statement).one()
        print("team_to_update", team_to_update)
        # statement2 = select(AppUser.id).where(
        #     (AppUser.first_name + " " + AppUser.last_name) == team.full_lead_name
        # )
        # user_lead_id_to_update = session.exec(statement2).one()

        # team_to_update.lead_user_id = user_lead_id_to_update
        team_to_update.short_name = team.short_name
        team_to_update.name = team.name
        team_to_update.is_active = team.is_active
        team_to_update.updated_at = datetime.now()
        # session.add(team_to_update)
        # session.refresh(team_to_update)
    session.commit()
    # return True
    # l.append(timelog_to_update)
