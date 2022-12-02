<script lang="ts">
	import { onMount } from 'svelte';
	import { baseUrl } from '../data/+server.js';
	import { getUsers, getRoles, getTeams } from '../data/+server.js';
	import EditableDatatable from '../../library/components/EditableDatatable.svelte';
	import Autocomplete from '../../library/components/autocomplete.svelte';
	import { clickOutside } from '/home/kateryna_iurieva/timeflow/frontend/src/clickOutside.js';
	import { Grid, Column, Row, Button } from '../../library/carbon/components';

	let users: Array<object> = [];
	let roles: Array<object> = [];
	let teams: Array<object> = [];
	let selectedRowIds: Array<string> = [];
	let newUserFirstName: string;
	let newUserLastName: string;
	let newUsername: string;
	let newEmail: string;
	let selectedRole: object = {};
	let selectedTeam: object = {};
	let selectedSupervisor: object = {};
	let startDate: string = '';
	let selectedEpic: Object = {};
	let updatedData: Array<object> = [];
	function handleClickOutside(event) {
		updatedData = [];
		selectedRowIds = [];
	}
	onMount(async () => {
		users = await getUsers();
		columnsToEdit.supervisor.options = users;
	});
	onMount(async () => {
		roles = await getRoles();
		columnsToEdit.role_name.options = roles;
	});
	onMount(async () => {
		teams = await getTeams();
		columnsToEdit.main_team.options = teams;
	});

	async function onSubmit() {
		const res = await fetch(`${baseUrl}/api/users/`, {
			method: 'POST',
			headers: { 'Content-type': 'application/json' },
			body: JSON.stringify({
				username: newUsername,
				first_name: newUserFirstName,
				last_name: newUserLastName,
				email: newEmail,
				role_id: selectedRole.id,
				team_id: selectedTeam.id,
				start_date: startDate,
				supervisor: selectedSupervisor.full_name,
				is_active: true,
				created_at: Date.now(),
				updated_at: Date.now()
			})
		});
		users = await getUsers();
	}
	async function onUpdate() {
		const updateRes = await fetch(`${baseUrl}/api/users/bulk_update`, {
			method: 'POST',
			headers: { 'Content-type': 'application/json' },
			body: JSON.stringify(updatedData)
		});
		users = await getUsers();
		updatedData = [];
		selectedRowIds = [];
	}
</script>

<!-- updatedData {JSON.stringify(updatedData)} -->
<Grid>
	<Row>
		<Column>
			<input class="month-picker" placeholder="first name" bind:value={newUserFirstName} />
		</Column>
		<Column>
			<input class="month-picker" placeholder="last name" bind:value={newUserLastName} />
		</Column>
		<Column>
			<input class="month-picker" placeholder="username" bind:value={newUsername} />
		</Column>
		<Column>
			<input class="month-picker" placeholder="email" bind:value={newEmail} />
		</Column>
	</Row>
	<Row>
		<Column>
			<Autocomplete
				options={roles}
				selectDisplay="role_name"
				bind:selectedOption={selectedRole}
				placeholder="select role"
			/>
		</Column>
		<Column>
			<Autocomplete
				options={teams}
				selectDisplay="team_name"
				bind:selectedOption={selectedTeam}
				placeholder="select team"
			/>
		</Column>
		<Column>
			<Autocomplete
				options={users}
				selectDisplay="full_name"
				bind:selectedOption={selectedSupervisor}
				placeholder="select supervisor"
			/>
		</Column>
		<Column>
			<input class="month-picker" type="date" bind:value={startDate} />
		</Column>
	</Row>
	<Row>
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
						{ key: 'username', value: 'USERNAME' },
						{ key: 'first_name', value: 'FIRST NAME' },
						{ key: 'last_name', value: 'LAST NAME' },
						{ key: 'role_name', value: 'ROLE' },
						{ key: 'main_team', value: 'MAIN_TEAM' },
						{ key: 'email', value: 'EMAIL' },
						{ key: 'start_date', value: 'START DATE' },
						{ key: 'supervisor', value: 'SUPERVISOR' },
						{ key: 'is_active', value: 'IS ACTIVE' }
					]}
					rows={users}
					bind:selectedRowIds
					bind:updatedData
					{onUpdate}
					columnsToEdit={{
						username: 'input',
						first_name: 'input',
						last_name: 'input',
						role_name: {
							type: 'autocomplete',
							selectDisplay: 'role_name',
							options: roles,
							placeholder: "role's name"
						},
						main_team: {
							type: 'autocomplete',
							selectDisplay: 'team_name',
							options: teams,
							placeholder: "teams's name"
						},
						epic_name: {
							type: 'autocomplete',
							selectDisplay: 'epic_name',
							options: roles,
							placeholder: "epic's name"
						},
						supervisor: {
							type: 'autocomplete',
							selectDisplay: 'full_name',
							options: users,
							placeholder: 'select supervisor'
						},
						is_active: 'toggle',
						email: 'input',
						start_date: 'date'
					}}
				/>
			</div>
		</Column>
	</Row>
</Grid>
