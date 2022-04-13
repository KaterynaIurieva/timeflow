import asyncio
from cProfile import label
import json
from black import click
from idom import html, run, use_state, component, event, vdom
import requests
from sanic import Sanic, response
from datetime import datetime

from components.input import Input
from components.layout import Row, Column, Container, FlexContainer
from components.lists import ListSimple
from components.table import SimpleTable, SubmitTable
from components.controls import Button

from config import base_url


@component
def page():
    name, set_name = use_state("")
    submitted_name, set_submitted_name = use_state("")
    deleted_name, set_deleted_name = use_state("")
    return FlexContainer(
        Column(width="3/12"),
        Column(
            Row(
                create_client_form(name, set_name, set_submitted_name),
                bg='bg-filter-block-bg'
            ),
            Column(
                Row(list_clients(submitted_name)),
            ),
            Row(delete_client(set_deleted_name)),
            width="6/12",
        ),
        Column(width="3/12"),
    )


@component
def create_client_form(name, set_name, set_submitted_name):
    """
        endpoint: /api/clients
        schema:
        {
      "name": "string",
      "active": True,
      "created_at": "2022-02-17T15:03:24.260Z",
      "updated_at": "2022-02-17T15:03:24.260Z"
    }"""

    @event(prevent_default=True)
    async def handle_submit(event):
        data = {
            "name": name,
            "is_active": True,
            "created_at": str(datetime.now()),
            "updated_at": str(datetime.now()),
        }
        print("here", data)
        response = requests.post(
            f"{base_url}/api/clients",
            data=json.dumps(data),
            headers={"accept": "application/json",
                     "Content-Type": "application/json"},
        )
        set_submitted_name(name)

    inp_name = Input(set_value=set_name, label="name")
    is_disabled = True
    if name != "":
        is_disabled = False
    btn = Button(is_disabled, handle_submit, label="Submit")

    return Column(
        Row(
            inp_name,
        ),
        Row(btn),
    )


@component
def list_clients_by_name(rows):
    return html.div({"class": "flex w-full"}, SimpleTable(rows=rows))


@component
def list_clients(submitted_name):
    api = f"{base_url}/api/clients/active"
    response = requests.get(api)

    rows = []
    for item in response.json():
        d = {
            "id": item["id"],
            "name": item["name"],
        }
        rows.append(d)
    return html.div({"class": "flex w-full"}, SubmitTable(rows=rows))


@component
def delete_client(set_deleted_name):
    client_id, set_client_id = use_state("")
    client_name, set_client_name = use_state("")

    def delete_client(event):
        api = f"{base_url}/api/clients/{client_id}?client_name={client_name}"
        response = requests.delete(api)
        set_deleted_name(client_name)
        print(f"state of deleted_name is {deleted_name}")

    inp_client_id = Input(set_value=set_client_id,
                          label="delete client:id input")
    inp_client_name = Input(set_value=set_client_name,
                            label="delete client:name input")
    btn = html.button(
        {
            "class": "relative w-fit h-fit px-2 py-1 text-lg border text-gray-50  border-secondary-200",
            "onClick": delete_client,
        },
        "Submit",
    )
    return Column(Row(inp_client_id, inp_client_name), Row(btn))
