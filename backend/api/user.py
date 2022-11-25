from fastapi import APIRouter, Depends
from ..utils import engine, get_session
from sqlmodel import Session, select
from sqlalchemy.exc import NoResultFound
from ..models.user import AppUser
from ..models.role import Role
from ..models.team import Team
from typing import Optional, List
from datetime import datetime, date
from pydantic import BaseModel

router = APIRouter(prefix="/api/users", tags=["user"])


@router.post("/")
async def post_user(
    user: AppUser,
    session: Session = Depends(get_session),
):
    """
    Post a new user.

    Parameters
    ----------
    user : User
        User that is to be added to the database.
    session : Session
        SQL session that is to be used to add the user.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(AppUser).where(AppUser.username == user.username)
    try:
        result = session.exec(statement).one()
        return False
    except NoResultFound:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


@router.get("/")
async def get_users(
    session: Session = Depends(get_session),
    is_active: bool = None,
    username: str = None,
):
    """
    Get list of user(s).

    Parameters
    ----------
    session : Session
        SQL session that is to be used to get the users.
        Defaults to creating a dependency on the running SQL model session.
    is_active : bool
        Status of users to be pulled.
    username : str
        Short name of user to be pulled.
    """
    statement = (
        select(
            AppUser.id,
            AppUser.username,
            AppUser.first_name,
            AppUser.last_name,
            AppUser.email,
            (AppUser.last_name + " " + AppUser.first_name).label("full_name"),
            Role.name.label("role_name"),
            Team.name.label("main_team"),
            AppUser.start_date,
            AppUser.supervisor,
            AppUser.is_active,
        )
        .select_from(AppUser)
        .join(Role, AppUser.role_id == Role.id, isouter=True)
        .join(Team, AppUser.team_id == Team.id, isouter=True)
    )

    if is_active != None:
        statement_final = (
            statement.where(AppUser.is_active == is_active)
            .order_by(AppUser.is_active.desc())
            .order_by(AppUser.first_name.asc())
            .order_by(AppUser.last_name.asc())
        )

    # elif username != None:
    #     statement_final = statement.select_from(AppUser).where(
    #         AppUser.username == username
    #     )
    else:
        statement_final = (
            statement.order_by(AppUser.is_active.desc())
            .order_by(AppUser.first_name.asc())
            .order_by(AppUser.last_name.asc())
        )

    result = session.exec(statement_final).all()
    return result


@router.get("/{user_id}")
async def get_user_by_id(user_id: int, session: Session = Depends(get_session)):
    statement = (
        select(
            AppUser.id,
            AppUser.username,
            AppUser.first_name,
            AppUser.last_name,
            Role.name.label("role_name"),
            Team.short_name.label("team_name"),
            AppUser.start_date,
            AppUser.is_active,
        )
        .select_from(AppUser)
        .join(Role, AppUser.role_id == Role.id, isouter=True)
        .join(Team, AppUser.team_id == Team.id, isouter=True)
    ).where(AppUser.id == user_id)
    result = session.exec(statement).all()
    return result


@router.put("/{user_id}/")
async def update_user(
    user_id: int,
    is_active: Optional[bool] = None,
    new_username: Optional[str] = None,
    new_first_name: Optional[str] = None,
    new_last_name: Optional[str] = None,
    new_email: Optional[str] = None,
    new_team_id: Optional[int] = None,
    new_role_id: Optional[int] = None,
    new_start_date: Optional[date] = None,
    new_supervisor: Optional[str] = None,
    session: Session = Depends(get_session),
):
    """
    Update a user.

    Parameters
    ----------
    user_id : int
        ID of user to be updated.
    is_active : Optional[bool]
        Updated status of user.
    new_username : Optional[str]
        Updated short name of user.
    new_first_name : Optional[str]
        Updated first name of user.
    new_last_name : Optional[str]
        Updated last name of user.
    new_email : Optional[str]
        Updated email of user
    new_team_id : Optional[int]
        Updated team id.
    new_role_id : Optional[int]
        Updated role id.
    new_start_date : Optional[date]
        Updated start date.
    session : Session
        SQL session that is to be used to update the user.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(AppUser).where(AppUser.id == user_id)
    user_to_update = session.exec(statement).one()
    if is_active != None:
        user_to_update.is_active = is_active
    if new_username != None:
        user_to_update.username = new_username
    if new_first_name != None:
        user_to_update.first_name = new_first_name
    if new_last_name != None:
        user_to_update.last_name = new_last_name
    if new_email != None:
        user_to_update.email = new_email
    if new_team_id != None:
        user_to_update.team_id = new_team_id
    if new_role_id != None:
        user_to_update.role_id = new_role_id
    if new_start_date != None:
        user_to_update.start_date = new_start_date
    if new_supervisor != None:
        user_to_update.supervisor = new_supervisor
    user_to_update.updated_at = datetime.now()
    session.add(user_to_update)
    session.commit()
    session.refresh(user_to_update)
    return user_to_update


class UpdateUser(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    role_name: str
    main_team: str
    supervisor: str = None
    start_date: date
    is_active: bool


@router.post("/bulk_update")
async def update_users(
    users: List[UpdateUser],
    session: Session = Depends(get_session),
):
    for user in users:
        statement = select(AppUser).where(AppUser.id == user.id)
        user_to_update = session.exec(statement).one()

        statement2 = select(Team.id).where(Team.name == user.main_team)
        team_id_to_update = session.exec(statement2).one()

        statement3 = select(Role.id).where(Role.name == user.role_name)
        role_id_to_update = session.exec(statement3).one()

        user_to_update.first_name = user.first_name
        user_to_update.last_name = user.last_name
        user_to_update.email = user.email
        user_to_update.role_id = role_id_to_update
        user_to_update.team_id = team_id_to_update
        if user.supervisor != None:
            user_to_update.supervisor = user.supervisor
        user_to_update.start_date = user.start_date
        user_to_update.is_active = user.is_active
        user_to_update.updated_at = datetime.now()
    session.commit()
