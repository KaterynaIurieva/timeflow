<script lang="ts">
	import { onMount } from 'svelte';
	import { baseUrl } from '../data/+server.js';
	import { getSponsors, getTeams, getEpics } from '../data/+server.js';
	import EditableDatatable from '../../library/components/EditableDatatable.svelte';
	import Autocomplete from '../../library/components/autocomplete.svelte';

	import { Grid, Column, Row, Button, TextInput } from '../../library/carbon/components';
	let epics = [{}];
	let teams = [{}];
	let sponsors: Array<object> = [{}];
	let selectedRowIds: Array<string> = [];
	let newEpicsFullName: string;
	let newEpicsShortName: string;
	// let columnsToEdit = {
	// 	epic_name: 'input',
	// 	short_name: 'input',
	// 	is_active: 'toggle',
	// 	team_name: {
	// 		input: 'autocomplete',
	// 		selectDisplay: 'team_name',
	// 		options: teams,
	// 		placeholder: "team's name"
	// 	},
	// 	sponsor_name: {
	// 		input: 'autocomplete',
	// 		selectDisplay: 'sponsor_name',
	// 		options: sponsors,
	// 		placeholder: "sponsor's name"
	// 	}
	// };

	let selectedTeam: Object = {};
	let selectedSponsor: Object = {};
	let startDate: string = '';
	let updatedData: Array<object> = [];
	onMount(async () => {
		epics = await getEpics();
	});

	onMount(async () => {
		sponsors = await getSponsors();
	});
	onMount(async () => {
		teams = await getTeams();
	});
	async function onSubmit() {
		const res = await fetch(`${baseUrl}/api/epics/`, {
			method: 'POST',
			headers: { 'Content-type': 'application/json' },
			body: JSON.stringify({
				team_id: selectedTeam.id,
				team_name: selectedTeam.team_name,
				sponsor_id: selectedSponsor.id,
				name: newEpicsFullName,
				short_name: newEpicsShortName,
				start_date: startDate,
				is_active: true,
				created_at: Date.now(),
				updated_at: Date.now()
			})
		});
		epics = await getEpics();
	}
	async function onUpdate() {
		const updateRes = await fetch(`${baseUrl}/api/epics/bulk_update`, {
			method: 'POST',
			headers: { 'Content-type': 'application/json' },
			body: JSON.stringify(updatedData)
		});
		epics = await getEpics();
		updatedData = [];
		selectedRowIds = [];
	}
</script>

<Grid>
	<Row>
		<Column>
			<TextInput placeholder="new epic's full name" bind:value={newEpicsFullName} />
		</Column>
		<Column>
			<TextInput placeholder="new epic's short name" bind:value={newEpicsShortName} />
		</Column>
		<Column>
			<input class="month-picker" type="date" bind:value={startDate} />
		</Column>
		<Autocomplete
			options={teams}
			selectDisplay="team_name"
			bind:selectedOption={selectedTeam}
			placeholder="select team"
		/>
		<Autocomplete
			options={sponsors}
			selectDisplay="sponsor_name"
			bind:selectedOption={selectedSponsor}
			placeholder="search sponsor"
		/>

		<Column>
			<Button size="small" kind="primary" on:click={onSubmit}>Submit</Button>
		</Column>
	</Row>
	<Row>
		<Column>
			<EditableDatatable
				headers={[
					{ key: 'id', value: 'ID' },
					{ key: 'epic_name', value: "FULL EPIC'S NAME" },
					{ key: 'short_name', value: "SHORT EPIC'S NAME" },
					{ key: 'team_name', value: "TEAM'S NAME" },
					{ key: 'sponsor_name', value: "SPONSORS'S NAME" },
					{ key: 'start_date', value: 'START DATE' },
					{ key: 'is_active', value: 'IS ACTIVE' }
				]}
				rows={epics}
				bind:selectedRowIds
				bind:updatedData
				{onUpdate}
				columnsToEdit={{
					epic_name: 'input',
					short_name: 'input',
					is_active: 'toggle',
					team_name: {
						type: 'autocomplete',
						selectDisplay: 'team_name',
						options: teams,
						placeholder: "team's name"
					},
					sponsor_name: {
						type: 'autocomplete',
						selectDisplay: 'sponsor_name',
						options: sponsors,
						placeholder: "sponsor's name"
					},
					start_date: 'date'
				}}
			/>
		</Column>
	</Row>
</Grid>
