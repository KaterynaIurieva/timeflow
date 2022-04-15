import requests
import json
from typing import TypedDict, List
from datetime import datetime
from config import base_url
from data.common import Select


class User(TypedDict):
    short_name: str
    first_name: str
    last_name: str
    email: str
    role_id: int
    team_id: int
    start_date: str
    created_at: datetime
    updated_at: datetime
    is_active: bool


def to_user(
    short_name: str,
    first_name: str,
    last_name: str,
    email: str,
    role_id: str,
    year_month: str,
    day: int,
    created_at: datetime,
    updated_at: datetime,
    team_id: str,
):
    ym = year_month
    year = ym[:4]
    month = ym[5:7]
    start_date = year + "-" + month + "-" + day

    data = User(
        short_name=short_name,
        first_name=first_name,
        last_name=last_name,
        email=email,
        role_id=role_id,
        team_id=team_id,
        start_date=start_date,
        created_at=str(created_at),
        updated_at=str(updated_at),
        is_active=True,
    )
    response = requests.post(
        f"{base_url}/api/users",
        data=json.dumps(dict(data)),
        headers={"accept": "application/json", "Content-Type": "application/json"},
    )


def users_active():
    api = f"{base_url}/api/users/"
    params = {"is_active": True}
    response = requests.get(api, params=params)
    rows = []
    for item in response.json():
        d = {
            "short name": item["short_name"],
            "first name": item["first_name"],
            "last name": item["last_name"],
            "role": item["role_short_name"],
            "main team": item["main_team"],
            "start date": item["start_date"],
        }
        rows.append(d)
    return rows


def update_user(user_id: int, new_team_id: int):
    api = f"{base_url}/api/users/{user_id}/"
    params = {"new_team_id": new_team_id}
    response = requests.put(api, params=params)
    return True


def activate_user(user_id: int):
    api = f"{base_url}/api/users/{user_id}/"
    params = {"is_active": True}
    response = requests.put(api, params=params)
    return True


def deactivate_user(user_id: int):
    api = f"{base_url}/api/users/{user_id}/"
    params = {"is_active": False}
    response = requests.put(api, params=params)
    return True


def users_names(label="select user") -> List[Select]:
    # Connect to users list endpoint
    api_user_name = f"{base_url}/api/users"
    response_user_name = requests.get(api_user_name)
    user_name_rows = [Select(value="", display_value=label)]
    for item in response_user_name.json():
        d = Select(value=item["id"], display_value=item["short_name"])
        user_name_rows.append(d)
    return user_name_rows
