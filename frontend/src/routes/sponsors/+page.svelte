<script lang="ts">
	import { onMount } from 'svelte';
	import { getSponsors } from '../data/+server.js';
	import { getClients } from '../data/+server.js';
	import { baseUrl } from '../data/+server.js';
	import EditableDatatable from '../../library/components/EditableDatatable.svelte';
	import Autocomplete from '../../library/components/autocomplete.svelte';
	import { clickOutside } from '../../library/components/clickOutside.js';
	import { Grid, Column, Row, Button, TextInput } from '../../library/carbon/components';
	let sponsors = [{}];
	let clients: Array<object> = [];
	let selectedRowIds: Array<string> = [];
	let newSponsorsFullName: string;
	let newSponsorsShortName: string;
	let selectedClient: Object = {};
	let updatedData: Array<object> = [];
	let columnsToEdit = {
		sponsor_name: 'input',
		sponsor_short_name: 'input',
		client_name: {
			type: 'autocomplete',
			selectDisplay: 'client_name',
			options: clients,
			placeholder: "client's name"
		},
		is_active: 'toggle'
	};

	if ((selectedRowIds = [])) {
		updatedData = [];
	}
	function handleClickOutside(event) {
		updatedData = [];
		selectedRowIds = [];
	}
	onMount(async () => {
		sponsors = await getSponsors();
	});
	onMount(async () => {
		clients = await getClients();
		columnsToEdit.client_name.options = clients;
	});

	async function onSubmit() {
		const res = await fetch(`${baseUrl}/api/sponsors/`, {
			method: 'POST',
			headers: { 'Content-type': 'application/json' },
			body: JSON.stringify({
				client_id: selectedClient.id,
				name: newSponsorsFullName,
				short_name: newSponsorsShortName,
				is_active: true,
				created_at: Date.now(),
				updated_at: Date.now()
			})
		});
		sponsors = await getSponsors();
	}
	async function onUpdate() {
		const updateRes = await fetch(`${baseUrl}/api/sponsors/bulk_update`, {
			method: 'POST',
			headers: { 'Content-type': 'application/json' },
			body: JSON.stringify(updatedData)
		});
		sponsors = await getSponsors();
		updatedData = [];
		selectedRowIds = [];
	}
</script>

<Grid>
	<Row>
		<Column>
			<TextInput placeholder="new sponsor's full name" bind:value={newSponsorsFullName} />
		</Column>
		<Column>
			<TextInput placeholder="new sponsor's short name" bind:value={newSponsorsShortName} />
		</Column>
		<Autocomplete
			options={clients}
			selectDisplay="client_name"
			bind:selectedOption={selectedClient}
			placeholder="search client"
		/>

		<Column>
			<Button size="small" kind="primary" on:click={onSubmit}>Submit</Button>
		</Column>
	</Row>
	<Row>
		<Column>
			<div use:clickOutside on:click_outside={handleClickOutside}>
				<EditableDatatable
					headers={[
						{ key: 'id', value: 'ID' },
						{ key: 'sponsor_name', value: "FULL SPONSOR'S NAME" },
						{ key: 'sponsor_short_name', value: "SHORT SPONSOR'S NAME" },
						{ key: 'client_name', value: "CLIENT'S NAME" },
						{ key: 'is_active', value: 'IS ACTIVE' }
					]}
					rows={sponsors}
					bind:selectedRowIds
					bind:updatedData
					{onUpdate}
					bind:columnsToEdit
				/>
			</div>
		</Column>
	</Row>
</Grid>
