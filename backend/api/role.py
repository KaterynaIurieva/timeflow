from fastapi import APIRouter, Depends
from ..utils import engine, get_session
from sqlmodel import Session, select, SQLModel
from sqlalchemy.exc import NoResultFound
from ..models.role import Role
from datetime import datetime

router = APIRouter(prefix="/api/roles", tags=["role"])
session = Session(engine)

# Post new role
@router.post("/")
async def post_role(*, role: Role, session: Session = Depends(get_session)):
    statement = select(Role).where(Role.id == role.id)
    try:
        result = session.exec(statement).one()
        return False
    except NoResultFound:
        session.add(role)
        session.commit()
        session.refresh(role)
        return role


# Get list of all roles
@router.get("/")
async def read_roles(session: Session = Depends(get_session)):
    statement = select(Role)
    results = session.exec(statement).all()
    return results


# Get list of active roles
@router.get("/active")
async def read_clients(session: Session = Depends(get_session)):
    statement = select(Client).where(Client.active == True)
    results = session.exec(statement).all()
    return results


@router.put("/{role_id}/activate")
async def activate_role(
    role_id: str = None,
    session: Session = Depends(get_session),
):
    statement = select(Role).where(Role.id == role_id)
    role_to_activate = session.exec(statement).one()
    role_to_activate.is_active = True
    role_to_activate.updated_at = datetime.now()
    session.add(role_to_activate)
    session.commit()
    session.refresh(role_to_activate)
    return role_to_activate


# Deactivate role
@router.put("/{role_id}/deactivate")
async def deactivate_role(
    role_id: str = None,
    session: Session = Depends(get_session),
):
    statement = select(Role).where(Role.id == role_id)
    role_to_deactivate = session.exec(statement).one()
    role_to_deactivate.is_active = False
    role_to_deactivate.updated_at = datetime.now()
    session.add(role_to_deactivate)
    session.commit()
    session.refresh(role_to_deactivate)
    return role_to_deactivate


# Update role
@router.put("/")
async def update_role(
    id: str = None,
    user_id: str = None,
    new_name: str = None,
    new_short_name: str = None,
    is_active: bool = None,
    session: Session = Depends(get_session),
):
    statement = select(Role).where(or_(Role.name == name, Role.id == id))
    role_to_update = session.exec(statement).one()
    role_to_update.user_id = user_id
    role_to_update.name = new_name
    role_to_update.short_name = new_short_name
    role_to_update.is_active = is_active
    session.add(role_to_update)
    role_to_update.updated_at = datetime.now()
    session.commit()
    session.refresh(role_to_update)
    return role_to_update
