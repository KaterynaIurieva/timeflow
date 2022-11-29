<script lang="ts">
	import { onMount } from 'svelte';
	import { getRate, getUsers, getClients } from '../data/+server.js';
	import { baseUrl } from '../data/+server.js';
	import EditableDatatable from '../../library/components/EditableDatatable.svelte';
	import Autocomplete from '../../library/components/autocomplete.svelte';
	import { Grid, Column, Row, Button, TextInput } from '../../library/carbon/components';
	import DateTimePicker from '../../library/components/DateTimePicker.svelte';
	let rates: any = [];
	let users: any = [];
	let clients: any = [];
	let selectedRowIds: Array<object> = [];
	let newRateUsername: string;
	let selectedClient: string;
	let newRateUserId: string;
	let startDate: string;
	const farDate: string = '9999-12-31';
	let newRateValidTo: string;
	// let columnsToEdit = {
	// 	is_active: 'toggle',
	// 	username: 'input'
	// };
	let updatedData: Array<object> = [];
	let result: any = null;

	onMount(async () => {
		rates = await getRate();
		console.log('rate', rates);
	});
	onMount(async () => {
		users = await getUsers(true);
	});
	onMount(async () => {
		clients = await getClients();
	});
	onMount(async () => {
		rates = await getRate();
	});
	async function onSubmit() {
		const res = await fetch(`${baseUrl}/api/rates/`, {
			method: 'POST',
			headers: { 'Content-type': 'application/json' },
			body: JSON.stringify({
				user_id: newRateUsername.id,
				client_id: selectedClient.id,
				valid_from: startDate,
				valid_to: farDate,
				amount: 0,
				created_at: Date.now(),
				updated_at: Date.now(),
				is_active: true
			})
		});
		console.log(
			'POST',
			JSON.stringify({
				user_id: newRateUsername.id,
				client_id: selectedClient.id,
				valid_from: startDate,
				amount: 0,
				created_at: Date.now(),
				updated_at: Date.now(),
				is_active: true
			})
		);
		const json = await res.json();
		result = JSON.stringify(json);
		rates = await getRate();
	}

	async function onUpdate() {
		const updateRes = await fetch(`${baseUrl}/api/rates/bulk_update`, {
			method: 'POST',
			headers: { 'Content-type': 'application/json' },
			body: JSON.stringify(updatedData)
		});
		rates = await getRate();
		updatedData = [];
		selectedRowIds = [];
	}
</script>

<Grid>
	<Row>
		<Column>
			<Autocomplete
				bind:selectedOption={newRateUsername}
				options={users}
				selectDisplay="username"
				placeholder="search user"
			/>
		</Column>
		<Column>
			<Autocomplete
				options={clients}
				selectDisplay="client_name"
				bind:selectedOption={selectedClient}
				placeholder="search client"
			/>
		</Column>
		<Column>
			<input class="month-picker" type="date" bind:value={startDate} />
		</Column>
		<Column>
			<Button size="small" kind="primary" on:click={onSubmit}>Submit</Button>
		</Column>
	</Row>
	<Row>
		<Column>
			<EditableDatatable
				headers={[
					{ key: 'id', value: 'ID' },
					{ key: 'full_name', value: 'FULL NAME' },
					{ key: 'name', value: 'CLIENT NAME' },
					{ key: 'valid_from', value: 'VALID FROM' },
					{ key: 'valid_to', value: 'VALID TO' },
					{ key: 'is_active', value: 'IS ACTIVE' }
				]}
				rows={rates}
				bind:selectedRowIds
				bind:updatedData
				{onUpdate}
				columnsToEdit={{
					full_name: {
						type: 'autocomplete',
						selectDisplay: 'full_name',
						options: users,
						placeholder: 'full name'
					},
					name: {
						type: 'autocomplete',
						selectDisplay: 'client_name',
						options: clients,
						placeholder: "client's name"
					},
					valid_from: 'date',
					valid_to: 'date',
					is_active: 'toggle'
				}}
			/>
		</Column>
	</Row>
</Grid>
