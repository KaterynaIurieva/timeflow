from fastapi import APIRouter, Depends
from ..utils import engine, get_session
from sqlmodel import Session, select
from sqlalchemy.exc import NoResultFound
from ..models.role import Role
from datetime import datetime
from typing import List
from pydantic import BaseModel

router = APIRouter(prefix="/api/roles", tags=["role"])


@router.post("/")
async def post_role(*, role: Role, session: Session = Depends(get_session)):
    """
    Post a new role.

    Parameters
    ----------
    role : Role
        Role that is to be added to the database.
    session : Session
        SQL session that is to be used to add the role.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Role).where(Role.id == role.id)
    try:
        result = session.exec(statement).one()
        return False
    except NoResultFound:
        session.add(role)
        session.commit()
        session.refresh(role)
        return role


@router.get("/")
async def read_roles(session: Session = Depends(get_session), is_active: bool = None):
    """
    Get list of all roles.

    Parameters
    ----------
    session : Session
        SQL session that is to be used to get the roles.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(
        Role.id,
        Role.name,
        Role.short_name,
        Role.is_active,
    )
    if is_active != None:
        statement_final = statement.where(Role.is_active == is_active).order_by(
            Role.is_active.desc()
        )
    else:
        statement_final = statement.order_by(Role.is_active.desc())
    results = session.exec(statement_final).all()
    return results


@router.put("/{role_id}/activate")
async def activate_role(
    role_id: str = None,
    session: Session = Depends(get_session),
):
    """
    Activate a role using the role ID as a key.

    Parameters
    ----------
    role_id : str
        ID of role to be activated.
    session : Session
        SQL session that is to be used to activate the role.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Role).where(Role.id == role_id)
    role_to_activate = session.exec(statement).one()
    role_to_activate.is_active = True
    role_to_activate.updated_at = datetime.now()
    session.add(role_to_activate)
    session.commit()
    session.refresh(role_to_activate)
    return role_to_activate


@router.put("/{role_id}/deactivate")
async def deactivate_role(
    role_id: str = None,
    session: Session = Depends(get_session),
):
    """
    Deactivate a role using the role ID as a key.

    Parameters
    ----------
    role_id : str
        ID of role to be deactivated.
    session : Session
        SQL session that is to be used to deactivate the role.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Role).where(Role.id == role_id)
    role_to_deactivate = session.exec(statement).one()
    role_to_deactivate.is_active = False
    role_to_deactivate.updated_at = datetime.now()
    session.add(role_to_deactivate)
    session.commit()
    session.refresh(role_to_deactivate)
    return role_to_deactivate


@router.put("/")
async def update_role(
    id: str = None,
    new_name: str = None,
    new_short_name: str = None,
    is_active: bool = None,
    session: Session = Depends(get_session),
):
    """
    Update a role.

    Parameters
    ----------
    id : str
        ID of role to be updated.
    new_name : str
        New name of the role.
    new_short_name : str
        New short name of the role.
    is_active : bool
        New status of the role.
    session : Session
        SQL session that is to be used to update the role.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Role.is_active).where(Role.id == id)
    result = session.exec(statement).first()
    if result == True:
        statement = select(Role).where(Role.id == id)
        role_to_update = session.exec(statement).one()
        if new_name != None:
            role_to_update.name = new_name
        if new_short_name != None:
            role_to_update.short_name = new_short_name
        if is_active != None:
            role_to_update.is_active = is_active
        session.add(role_to_update)
        role_to_update.updated_at = datetime.now()
        session.commit()
        session.refresh(role_to_update)
        return role_to_update
    else:
        return False


class UpdateRole(BaseModel):
    id: int
    name: str
    short_name: str
    is_active: bool


@router.post("/bulk_update")
async def update_roles(
    roles: List[UpdateRole],
    session: Session = Depends(get_session),
):
    for role in roles:
        statement = select(Role).where(Role.id == role.id)
        role_to_update = session.exec(statement).one()

        role_to_update.name = role.name
        role_to_update.short_name = role.short_name
        role_to_update.is_active = role.is_active
        role_to_update.updated_at = datetime.now()
        session.add(role_to_update)
        # session.refresh(timelog_to_update)
    session.commit()
    return True
    # l.append(timelog_to_update)
