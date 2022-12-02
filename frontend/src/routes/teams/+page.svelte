<script lang="ts">
	import { onMount } from 'svelte';
	import { baseUrl } from '../data/+server.js';
	import { getTeams } from '../data/+server.js';
	import { getUsers } from '../data/+server.js';
	import EditableDatatable from '../../library/components/EditableDatatable.svelte';
	import Autocomplete from '../../library/components/autocomplete.svelte';

	import { Grid, Column, Row, Button, TextInput } from '../../library/carbon/components';
	import { clickOutside } from '/home/kateryna_iurieva/timeflow/frontend/src/clickOutside.js';
	let teams = [{}];
	let users: [{}];
	let selectedRowIds: Array<string> = [];
	let newTeamsFullName: string;
	let newTeamsShortName: string;
	let selectedUser: Object = {};
	let updatedData: Array<object> = [];

	function handleClickOutside(event) {
		updatedData = [];
		selectedRowIds = [];
	}
	onMount(async () => {
		teams = await getTeams();
	});
	onMount(async () => {
		users = await getUsers(true);
	});
	async function onSubmit() {
		const res = await fetch(`${baseUrl}/api/teams/`, {
			method: 'POST',
			headers: { 'Content-type': 'application/json' },
			body: JSON.stringify({
				lead_user_id: selectedUser.id,
				name: newTeamsFullName,
				short_name: newTeamsShortName,
				is_active: true,
				created_at: Date.now(),
				updated_at: Date.now()
			})
		});
		teams = await getTeams();
	}
	async function onUpdate() {
		const updateRes = await fetch(`${baseUrl}/api/teams/bulk_update`, {
			method: 'POST',
			headers: { 'Content-type': 'application/json' },
			body: JSON.stringify(updatedData)
		});
		teams = await getTeams();
		updatedData = [];
		selectedRowIds = [];
	}
</script>

<Grid>
	<Row>
		<Column>
			<TextInput placeholder="new team's full name" bind:value={newTeamsFullName} />
		</Column>
		<Column>
			<TextInput placeholder="new team's short name" bind:value={newTeamsShortName} />
		</Column>
		<Autocomplete
			options={users}
			selectDisplay="full_name"
			bind:selectedOption={selectedUser}
			placeholder="select user lead"
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
						{ key: 'name', value: "FULL TEAM'S NAME" },
						{ key: 'short_name', value: "SHORT TEAM'S NAME" },
						{ key: 'full_lead_name', value: 'USER LEAD' },
						{ key: 'is_active', value: 'IS ACTIVE' }
					]}
					rows={teams}
					bind:selectedRowIds
					bind:updatedData
					{onUpdate}
					columnsToEdit={{
						name: 'input',
						short_name: 'input',
						full_lead_name: {
							type: 'autocomplete',
							selectDisplay: 'full_name',
							options: users,
							placeholder: 'user lead'
						},
						is_active: 'toggle'
					}}
				/>
			</div>
		</Column>
	</Row>
</Grid>
