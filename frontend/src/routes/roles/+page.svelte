<script lang="ts">
	import { onMount } from 'svelte';
	import { getRoles } from '../data/+server.js';
	import { baseUrl } from '../data/+server.js';
	import EditableDatatable from '../../library/components/EditableDatatable.svelte';
	import Autocomplete from '../../library/components/autocomplete.svelte';
	import { clickOutside } from '/home/kateryna_iurieva/timeflow/frontend/src/clickOutside.js';
	import { Grid, Column, Row, Button, TextInput } from '../../library/carbon/components';
	let roles = [{}];
	let selectedRowIds: Array<string> = [];
	let newRolesFullName: string;
	let newRolesShortName: string;
	let columnsToEdit = ['name', 'short_name', 'is_active'];
	let updatedData: Array<object> = [];
	let result: any = null;
	function handleClickOutside(event) {
		updatedData = [];
		selectedRowIds = [];
	}
	onMount(async () => {
		roles = await getRoles();
		console.log('roles', roles);
	});
	async function onSubmit() {
		const res = await fetch(`${baseUrl}/api/roles/`, {
			method: 'POST',
			headers: { 'Content-type': 'application/json' },
			body: JSON.stringify({
				name: newRolesFullName,
				short_name: newRolesShortName,
				is_active: true,
				created_at: Date.now(),
				updated_at: Date.now()
			})
		});
		const json = await res.json();
		result = JSON.stringify(json);
		roles = await getRoles();
	}
	async function onUpdate() {
		const updateRes = await fetch(`${baseUrl}/api/roles/bulk_update`, {
			method: 'POST',
			headers: { 'Content-type': 'application/json' },
			body: JSON.stringify(updatedData)
		});
		roles = await getRoles();
		updatedData = [];
		selectedRowIds = [];
	}
</script>

<Grid>
	<Row>
		<Column>
			<TextInput placeholder="new role's full name" bind:value={newRolesFullName} />
		</Column>
		<Column>
			<TextInput placeholder="new role's short name" bind:value={newRolesShortName} />
		</Column>

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
						{ key: 'role_name', value: "FULL ROLE'S NAME" },
						{ key: 'short_name', value: "SHORT ROLE'S NAME" },
						{ key: 'is_active', value: 'IS ACTIVE' }
					]}
					rows={roles}
					bind:selectedRowIds
					bind:updatedData
					{onUpdate}
					columnsToEdit={{
						role_name: 'input',
						short_name: 'input',
						is_active: 'toggle'
					}}
				/>
			</div>
		</Column>
	</Row>
</Grid>
