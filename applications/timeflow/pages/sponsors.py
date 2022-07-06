from idom import html, use_state, component, event

from uiflow.components.controls import (
    activation_button,
    deactivation_button,
    submit_button,
    Button,
)
from uiflow.components.input import Input, Selector
from uiflow.components.layout import Row, Column, Container
from uiflow.components.table import SimpleTable

from ..data.sponsors import (
    get_active_sponsor_rows,
    post_sponsor,
    sponsor_activation,
    sponsor_deactivation,
    sponsor_names,
)
from ..data.clients import clients_names


@component
def page(key_attr: str):
    name, set_name = use_state("")
    submitted_name, set_submitted_name = use_state("")
    short_name, set_short_name = use_state("")
    submitted_short_name, set_submitted_short_name = use_state("")
    client_id, set_client_id = use_state("")
    _, set_deact_name = use_state("")
    _, set_activ_name = use_state("")

    return html.div(
        {"class": "w-full", "key": key_attr},
        Row(
            create_sponsor_form(
                name,
                set_name,
                short_name,
                set_short_name,
                client_id,
                set_client_id,
                set_submitted_name,
                set_submitted_short_name,
            ),
            bg="bg-filter-block-bg",
        ),
        Container(
            Column(
                Row(list_sponsors(submitted_name, submitted_short_name)),
            ),
            Row(deactivate_sponsor(set_deact_name)),
            Row(activate_sponsor(set_activ_name)),
        ),
    )


@component
def create_sponsor_form(
    name,
    set_name,
    short_name,
    set_short_name,
    client_id,
    set_client_id,
    set_submitted_name,
    set_submitted_short_name,
):
    """
    Create a form that allows admin to add a new sponsor.

    post endpoint: /api/sponsors
    schema: {
        "name": "string",
        "short_name": "string",
        "client_id": "int",
        "is_active": True
        "created_at": "2022-02-17T15:31:39.103Z",
        "updated_at": "2022-02-17T15:31:39.103Z"
    }
    """

    @event(prevent_default=True)
    async def handle_submit(event):
        """Call a post request for the given sponsor when given event is triggered."""
        post_sponsor(name, short_name, client_id)

        # Change the states
        set_submitted_name(name)
        set_submitted_short_name(short_name)

    # Create input field for the name of the sponsor
    inp_name = Input(
        set_value=set_name,
        label="full name of the sponsor",
        width="[32%]",
        md_width="[32%]",
    )

    # Create input field for the short name of the sponsor
    inp_short_name = Input(
        set_value=set_short_name,
        label="short name of the sponsor",
        width="[32%]",
        md_width="[32%]",
    )

    # Create a dropdown of clients which can then be selected
    selector_client_id = Selector(
        set_value=set_client_id,
        data=clients_names(is_active=True),
        width="32%",
        md_width="32%",
    )

    # Create submit button
    btn = submit_button(handle_submit, name, short_name, client_id)

    return Container(
        Column(
            Row(
                inp_name, inp_short_name, selector_client_id, justify="justify-between"
            ),
            Row(btn),
        )
    )


@component
def list_sponsors(submitted_name, submitted_short_name):
    """
    Return rows consisting of each sponsor along with its client.

    Obtain a json response from a get request to the client endpoint.
    Store in rows the names of the client and sponsor, along with the id.
    Return an HTML div that contains the rows in a table.
    """
    rows = get_active_sponsor_rows()
    return html.div({"class": "flex w-full"}, SimpleTable(rows=rows))


@component
def deactivate_sponsor(set_deact_name):
    """Deactivate a sponsor without deleting it."""
    name_to_deact, set_name_to_deact = use_state("")

    def handle_deactivation(event):
        """Set the given sponsor's active column to False."""
        sponsor_deactivation(name_to_deact)
        set_deact_name(name_to_deact)

    # Create input field for name of sponsor to be deactivated
    sponsors_selector_deact = Selector(
        set_name_to_deact,
        data=sponsor_names(is_active=True, label="sponsor to be deactivated"),
        width="96%",
        md_width="96%",
    )

    # Create the deactivation button
    is_disabled = True
    if name_to_deact != "":
        is_disabled = False
    btn = Button(is_disabled, handle_submit=handle_deactivation, label="Deactivate")
    return Column(Row(sponsors_selector_deact), Row(btn))


@component
def activate_sponsor(set_activ_name):
    """Activate a sponsor."""
    name_to_activ, set_name_to_activ = use_state("")

    def handle_activation(event):
        """Set the given sponsor's active column to True."""
        sponsor_activation(name_to_activ)
        set_activ_name(name_to_activ)

    # Create input field for name of sponsor to be activated
    sponsors_selector_act = Selector(
        set_name_to_activ,
        data=sponsor_names(is_active=False, label="sponsor to be activated"),
        width="96%",
        md_width="96%",
    )

    # Create the activation button
    is_disabled = True
    if name_to_activ != "":
        is_disabled = False
    btn = Button(is_disabled, handle_submit=handle_activation, label="Activate")
    return Column(Row(sponsors_selector_act), Row(btn))
