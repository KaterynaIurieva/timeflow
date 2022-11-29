<script lang="ts">
	import 'carbon-components-svelte/css/white.css';
	import { onMount } from 'svelte';
	import { baseUrl } from '../data/+server.js';
	import { Grid, Column, Row, Button } from '../../library/carbon/components';
	import { getTimelogs, getUsers, getEpics, getEpicAreas } from '../data/+server.js';
	import Autocomplete from '../../library/components/autocomplete.svelte';
	import EditableDatatable from '../../library/components/EditableDatatable.svelte';
	import DateTimePicker from '../../library/components/DateTimePicker.svelte';
	let users: any[];
	let epics: any[];
	let epicAreas: any;
	let epicAreasSelect: any;
	let timelogs: any = [];
	let timelog = {
		username: '',
		epicName: '',
		epicAreaName: '',
		startTime: new Date(),
		endTime: new Date()
	};
	let selectedEpic = { id: '', epic_name: '' };
	let selectedEpicArea = { id: '', epic_area_name: '' };
	let startTime: string;
	let endTime: string;
	let result: any = null;
	let selectedUser = { id: '', username: '' };
	let selectedRowIds: any = [];
	let updatedData: Array<object> = [];
	let updateRes: any;
	let columnsToEdit = ['start_time', 'end_time'];

	onMount(async () => {
		users = await getUsers(true);
	});
	onMount(async () => {
		epicAreas = await getEpicAreas();
	});
	onMount(async () => {
		epics = await getEpics();
	});
	onMount(async () => {
		timelogs = await getTimelogs(timelogs);
	});

	async function onSubmit() {
		let startTimeDate = new Date(startTime);
		const res = await fetch(`${baseUrl}/api/timelogs/`, {
			method: 'POST',
			headers: { 'Content-type': 'application/json' },
			body: JSON.stringify({
				user_id: selectedUser.id,
				start_time: startTime,
				end_time: endTime,
				epic_id: selectedEpic.id,
				epic_area_id: selectedEpicArea.id,
				count_hours: 1,
				count_days: 1,
				month: startTimeDate.getMonth() + 1,
				year: startTimeDate.getFullYear(),
				created_at: Date.now(),
				updated_at: Date.now(),
				is_locked: false
			})
		});
		const json = await res.json();
		result = JSON.stringify(json);
		timelogs = await getTimelogs(timelogs);
	}

	async function onRemove() {
		async function DeleteApi(id: number) {
			const response = await fetch(`${baseUrl}/api/timelogs/` + id, {
				method: 'DELETE',
				headers: {
					'Content-type': 'application/json'
				}
			});
			timelogs = await getTimelogs(timelogs);
		}
		selectedRowIds.map(DeleteApi);
	}

	async function epicAreasByEpic(selectedEpic: any) {
		const response = await fetch(`${baseUrl}/api/epic_areas/?epic_id=` + selectedEpic.id, {
			method: 'GET',
			headers: { 'Content-type': 'application/json' }
		});
		epicAreasSelect = await response.json();
		return epicAreas;
	}
</script>

<Grid>
	<Row>
		<Column>
			<Autocomplete
				bind:selectedOption={selectedUser}
				options={users}
				selectDisplay="username"
				placeholder="search user"
			/>
		</Column>
		<Column>
			<Autocomplete
				bind:selectedOption={selectedEpic}
				options={epics}
				selectDisplay="epic_name"
				placeholder="search epic"
				onChange={epicAreasByEpic}
			/>
		</Column>
		<Column>
			{#key selectedEpic.id}
				<Autocomplete
					bind:selectedOption={selectedEpicArea}
					options={epicAreasSelect}
					selectDisplay="epic_area_name"
					placeholder="search epic area"
				/>
			{/key}
		</Column>

		<Column>
			<DateTimePicker bind:value={startTime} />
		</Column>
		<Column>
			<DateTimePicker bind:value={endTime} />
		</Column>
		<Column>
			<Button on:click={onSubmit} size="small" kind="primary">Submit</Button>
		</Column>
	</Row>
	<Row>
		<Column>
			<EditableDatatable
				headers={[
					{ key: 'id', value: 'ID' },
					{ key: 'username', value: 'USERAME' },
					{ key: 'epic_name', value: 'EPIC NAME' },
					{ key: 'epic_area_name', value: 'EPIC AREA NAME' },
					{ key: 'start_time', value: 'START TIME' },
					{ key: 'end_time', value: 'END TIME' },
					{ key: 'count_hours', value: 'COUNT HOURS' },
					{ key: 'count_days', value: 'COUNT DAYS' }
				]}
				rows={timelogs}
				{columnsToEdit}
				bind:selectedRowIds
				{onRemove}
				bind:updatedData
			/>
		</Column>
	</Row>
</Grid>
