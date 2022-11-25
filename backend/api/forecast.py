from fastapi import APIRouter, Depends
from ..utils import engine, get_session
from ..models.forecast import Forecast
from ..models.epic import Epic
from ..models.user import AppUser
from ..models.epic_area import EpicArea
from sqlmodel import Session, select, and_
from sqlalchemy.exc import NoResultFound
from sqlalchemy import func
from datetime import datetime, date
from pydantic import BaseModel
from typing import Optional, List


router = APIRouter(prefix="/api/forecasts", tags=["forecast"])


@router.post("/")
async def post_forecast(*, forecast: Forecast, session: Session = Depends(get_session)):
    """
    Post a new forecast.
    Parameters
    ----------
    forecast : Forecast
        Forecast that is to be added to the database.
    session : Session
        SQL session that is to be used to add the forecast.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Forecast).where(
        and_(
            Forecast.epic_id == forecast.epic_id,
            Forecast.user_id == forecast.user_id,
            Forecast.year == forecast.year,
            Forecast.month == forecast.month,
        )
    )
    try:
        result = session.exec(statement).one()
        return "A forecast for selected user, month and epic already exists"
    except NoResultFound:
        session.add(forecast)
        session.commit()
        session.refresh(forecast)
        return "Your forecast has been submitted"


@router.get("/")
async def get_forecasts(
    epic_id: int = None,
    month: int = None,
    year: int = None,
    session: Session = Depends(get_session),
):
    """
    Get list of forecasts.
    Parameters
    ----------
    session : Session
        SQL session that is to be used to get a list of the forecasts.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = (
        select(
            Forecast.id,
            AppUser.username,
            AppUser.first_name,
            AppUser.last_name,
            (AppUser.last_name + " " + AppUser.first_name).label("full_name"),
            Epic.name.label("epic_name"),
            Epic.id.label("epic_id"),
            Forecast.year,
            Forecast.month,
            Forecast.days.label("forecast_days"),
        )
        .select_from(Forecast)
        .join(AppUser)
        .join(Epic)
    )
    if month != None and year != None and epic_id != None:
        final_statement = (
            select(
                Epic.name.label("epic_name"),
                Forecast.year,
                Forecast.month,
                func.sum(Forecast.days).label("forecast_days_sum"),
            )
            .select_from(Forecast)
            .join(Epic)
            .where(Epic.id == epic_id)
            .where(Forecast.month == month)
            .where(Forecast.year == year)
            .group_by(Epic.name, Forecast.month, Forecast.year)
            .order_by(Forecast.year.desc())
            .order_by(Forecast.month.desc())
            .order_by(Forecast.days.desc())
            .order_by(Epic.name.asc())
            .order_by(AppUser.username.asc())
        )

    else:
        final_statement = (
            statement.order_by(Forecast.year.asc())
            # .where(Forecast.year >= datetime.now().year)
            # .where(Forecast.month >= datetime.now().month)
            .order_by(Forecast.year.desc())
            .order_by(Forecast.month.desc())
            .order_by(Forecast.days.desc())
            .order_by(Epic.name.asc())
            .order_by(AppUser.username.asc())
        )

    result = session.exec(final_statement).all()
    return result


@router.get("/users/{user_id}")
async def get_forecasts_by_user(
    user_id: str = None,
    session: Session = Depends(get_session),
    year: str = None,
    month: str = None,
):
    """
    Get forecasts from a given user.
    Parameters
    ----------
    user_id : str
        User ID of user from which forecasts are to be pulled from.
    session : Session
        SQL session that is to be used to get the forecasts.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = (
        select(
            Forecast.id,
            AppUser.username,
            AppUser.first_name,
            AppUser.last_name,
            Epic.name.label("epic_name"),
            Forecast.year,
            Forecast.month,
            Forecast.days.label("forecast_days"),
        )
        .select_from(Forecast)
        .join(AppUser)
        .join(Epic)
        .where(Forecast.user_id == user_id)
    )
    if year != None and month != None:
        final_statement = (
            statement.where(Forecast.year == year)
            .where(Forecast.month == month)
            .order_by(Forecast.year.desc())
            .order_by(Forecast.month.desc())
            .order_by(Forecast.days.desc())
            .order_by(Epic.name.asc())
            .order_by(AppUser.username.asc())
        )
    else:
        final_statement = (
            statement.where(Forecast.year >= datetime.now().year)
            .where(Forecast.month >= datetime.now().month)
            .order_by(Forecast.year.desc())
            .order_by(Forecast.month.desc())
            .order_by(Forecast.days.desc())
            .order_by(Epic.name.asc())
            .order_by(AppUser.username.asc())
        )

    result = session.exec(final_statement).all()
    return result


@router.get("/users/{user_id}/epics/{epic_id}")
async def get_forecasts_by_user_year_epic(
    user_id: str, epic_id: str, session: Session = Depends(get_session)
):
    """
    Get forecast by user and epic
    Parameters
    ----------
    user_id : str
        User ID of user from which to pull forecasts from.
    epic_id : str
        Epic ID of epic from which to pull forecasts from.
    session : Session
        SQL session that is to be used to get the forecasts.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = (
        select(Forecast.month, Forecast.days)
        .where(Forecast.user_id == user_id)
        .where(Forecast.epic_id == epic_id)
    )
    results = session.exec(statement).all()
    return results


@router.get("/users/{user_id}/epics/year/{year}/month/{month}")
async def get_forecasts_by_user_year_epic(
    user_id, year, month, session: Session = Depends(get_session)
):
    """
    Get forecast by user ID, month, and year.
    Parameters
    ----------
    user_id
        ID of user from which to pull forecasts from.
    year
        Year from which to pull forecasts from.
    month
        Month from which to pull forecasts from.
    session : Session
        SQL session that is to be used to get the forecasts.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = (
        select(
            Forecast.id,
            AppUser.username,
            Epic.name.label("epic_name"),
            Forecast.year,
            Forecast.month,
            Forecast.days.label("forecast_days"),
        )
        .select_from(Forecast)
        .join(AppUser)
        .join(Epic)
        .where(Forecast.user_id == user_id)
        .where(Forecast.year == year)
        .where(Forecast.month == month)
    )
    results = session.exec(statement).all()
    return results


@router.get("/users/{user_id}/epics/{epic_id}/year/{year}/month/{month}")
async def get_forecasts_by_user_year_epic(
    user_id, epic_id, year, month, session: Session = Depends(get_session)
):
    """
    Get forecast by user, epic, year, month
    Parameters
    ----------
    user_id
        ID of user from which to pull forecasts from.
    epic_id
        ID of epic from which to pull forecasts from.
    year
        Year from which to pull forecasts from.
    month
        Month from which to pull forecasts from.
    session : Session
        SQL session that is to be used to get the forecasts.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = (
        select(
            Forecast.id,
            AppUser.username,
            Epic.name.label("epic_name"),
            Forecast.year,
            Forecast.month,
            Forecast.days.label("forecast_days"),
        )
        .select_from(Forecast)
        .join(AppUser)
        .join(Epic)
        .where(Forecast.user_id == user_id)
        .where(Forecast.epic_id == epic_id)
        .where(Forecast.year == year)
        .where(Forecast.month == month)
    )
    results = session.exec(statement).all()
    return results


@router.delete("/")
async def delete_forecasts(
    forecast_id: str = None,
    session: Session = Depends(get_session),
):
    """
    Delete a forecast
    Parameters
    ----------
    forecast_id : str
        ID of forecast to delete.
    session : Session
        SQL session that is to be used to delete the forecast.
        Defaults to creating a dependency on the running SQL model session.
    """
    statement = select(Forecast).where(
        Forecast.id == forecast_id,
    )

    forecast_to_delete = session.exec(statement).one()
    session.delete(forecast_to_delete)
    session.commit()
    return True


class UpdateForecast(BaseModel):
    id: int
    forecast_days: float


@router.post("/bulk_update")
async def update_forecasts(
    forecasts: List[UpdateForecast],
    session: Session = Depends(get_session),
):
    for forecast in forecasts:
        statement = select(Forecast).where(Forecast.id == forecast.id)
        forecast_to_update = session.exec(statement).one()
        forecast_to_update.days = forecast.forecast_days
        forecast_to_update.updated_at = datetime.now()
    session.commit()
