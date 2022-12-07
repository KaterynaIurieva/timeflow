<script lang="ts">
	import { getClients } from '../data/+server.js';
	import { onMount } from 'svelte';
	import { baseUrl } from '../data/+server.js';
	import EditableDatatable from '../../library/components/EditableDatatable.svelte';
	import { clickOutside } from '../../library/components/clickOutside.js';
	import {
		Grid,
		Column,
		Row,
		DataTable,
		Button,
		Pagination,
		Toolbar,
		ToolbarBatchActions,
		TextInput,
		Toggle
	} from '../../library/carbon/components';

	let newClientsName: string;
	let clients = [{}];
	let selectedRowIds: Array<string> = [];

	let updatedData: Array<object> = [];
	function handleClickOutside(event) {
		updatedData = [];
		selectedRowIds = [];
	}
	onMount(async () => {
		clients = await getClients();
	});
	async function onSubmit() {
		const res = await fetch(`${baseUrl}/api/clients/`, {
			method: 'POST',
			headers: { 'Content-type': 'application/json' },
			body: JSON.stringify({
				name: newClientsName,
				is_active: true,
				created_at: Date.now(),
				updated_at: Date.now()
			})
		});
		clients = await getClients();
	}
	async function onUpdate() {
		const updateRes = await fetch(`${baseUrl}/api/clients/bulk_update`, {
			method: 'POST',
			headers: { 'Content-type': 'application/json' },
			body: JSON.stringify(updatedData)
		});
		clients = await getClients();
		updatedData = [];
		selectedRowIds = [];
	}
</script>

<Grid>
	<Row>
		<Column>
			<TextInput placeholder="new client's name" bind:value={newClientsName} />
		</Column>
		<Column>
			<Button size="small" kind="primary" on:click={onSubmit}>Submit</Button>
		</Column>
		<Column />
	</Row>
	<Row>
		<Column>
			<div use:clickOutside on:click_outside={handleClickOutside}>
				<EditableDatatable
					headers={[
						{ key: 'id', value: 'ID' },
						{ key: 'client_name', value: 'NAME' },
						{ key: 'is_active', value: 'IS ACTIVE' }
					]}
					rows={clients}
					bind:selectedRowIds
					bind:updatedData
					{onUpdate}
					columnsToEdit={{
						client_name: 'input',
						is_active: 'toggle'
					}}
				/>
			</div>
		</Column>
	</Row>
</Grid>
