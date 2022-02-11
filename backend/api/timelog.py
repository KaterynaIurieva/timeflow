from fastapi import APIRouter, Depends
from ..utils import engine, string_to_datetime, get_session
from sqlmodel import Session, select, SQLModel, or_
from ..utils import engine
from ..models.user import User
from ..models.timelog import TimeLog

router = APIRouter(prefix="/api/timelogs", tags=["timelog"])


# Post timelog
# example: timelog.start_time = "2022-01-19T08:30:00.000Z"
@router.post("/")
async def timelog(*, timelog: TimeLog, session: Session = Depends(get_session)):
    statement1 = (
        select(TimeLog)
        .where(TimeLog.user_id == timelog.user_id)
        .where(TimeLog.start_time >= timelog.start_time)
        .where(TimeLog.start_time <= timelog.end_time)
    )
    statement2 = (
        select(TimeLog)
        .where(TimeLog.user_id == timelog.user_id)
        .where(TimeLog.end_time >= timelog.start_time)
        .where(TimeLog.end_time <= timelog.end_time)
    )
    results1 = session.exec(statement1).all()
    results2 = session.exec(statement2).all()
    if results1 or results2:
        return "currently posted timelog overlaps another timelog"
    else:
        session.add(timelog)
        session.commit()
        session.refresh(timelog)
        return timelog


# Get all timelogs
@router.get("/")
async def get_timelogs_all(session: Session = Depends(get_session)):
    statement = select(TimeLog)
    results = session.exec(statement).all()
    return results


# Get timelog by id
@router.get("/{timelog_id}")
async def get_timelog_by_id(timelog_id: int, session: Session = Depends(get_session)):
    statement = select(TimeLog).where(TimeLog.id == timelog_id)
    result = session.exec(statement).one()
    return result


# Get list of timelogs by user_id, month
@router.get("/users/{user_id}/months/{month}/years/{year}")
async def get_timelog_user_id(
    *,
    user_id: str,
    month: int,
    year: int,
    session: Session = Depends(get_session),
):
    statement = (
        select(TimeLog)
        .where(TimeLog.user_id == user_id)
        .where(TimeLog.month == month)
        .where(TimeLog.year == year)
    )
    results = session.exec(statement).all()
    return results


# Update timelogs
@router.put("/{timelog_id}/new-start-time")
async def update_timelogs(
    *,
    timelog_id: int = None,
    timelog_new_start_time: str = None,
    session: Session = Depends(get_session),
):
    statement = select(TimeLog).where(TimeLog.id == timelog_id)
    timelog_to_update = session.exec(statement).one()
    timelog_to_update.start_time = timelog_new_start_time
    session.add(timelog_to_update)
    session.commit()
    session.refresh(timelog_to_update)
    return timelog_to_update


# Delete timelogs
@router.delete("/{timelog_id}")
async def delete_timelogs(
    *,
    timelog_id: int,
    session: Session = Depends(get_session),
):
    statement = select(TimeLog).where(TimeLog.id == timelog_id)
    result = session.exec(statement).one()
    timelog_to_delete = result
    session.delete(timelog_to_delete)
    session.commit()
    return True
