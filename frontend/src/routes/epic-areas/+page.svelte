<script lang="ts">
	import { onMount } from 'svelte';
	import { baseUrl } from '../data/+server.js';
	import { getEpics } from '../data/+server.js';
	import { getEpicAreas } from '../data/+server.js';
	import EditableDatatable from '../../library/components/EditableDatatable.svelte';
	import Autocomplete from '../../library/components/autocomplete.svelte';
	import DateTimePicker from '../../library/components/DateTimePicker.svelte';

	import { Grid, Column, Row, Button, TextInput } from '../../library/carbon/components';
	let epics: Array<object> = [];
	let epicAreas: Array<object> = [];
	let selectedRowIds: Array<string> = [];
	let newEpicAreaName: string;
	let startDate: string = '';
	let selectedEpic: Object = {};
	let updatedData: Array<object> = [];

	let columnsToEdit = {
		epic_area_name: 'input',
		epic_name: {
			type: 'autocomplete',
			selectDisplay: 'epic_name',
			options: epics,
			placeholder: "epic's name"
		},
		is_active: 'toggle'
	};

	onMount(async () => {
		epics = await getEpics();
		columnsToEdit.epic_name.options = epics;
	});
	onMount(async () => {
		epicAreas = await getEpicAreas();
	});

	async function onSubmit() {
		const res = await fetch(`${baseUrl}/api/epic_areas/`, {
			method: 'POST',
			headers: { 'Content-type': 'application/json' },
			body: JSON.stringify({
				epic_id: selectedEpic.id,
				name: newEpicAreaName,
				start_date: startDate,
				is_active: true,
				created_at: Date.now(),
				updated_at: Date.now()
			})
		});
		epicAreas = await getEpicAreas();
	}
	async function onUpdate() {
		const updateRes = await fetch(`${baseUrl}/api/epic_areas/bulk_update`, {
			method: 'POST',
			headers: { 'Content-type': 'application/json' },
			body: JSON.stringify(updatedData)
		});
		epicAreas = await getEpicAreas();
		updatedData = [];
		selectedRowIds = [];
	}
</script>

<!-- updatedData {JSON.stringify(updatedData)} -->
<Grid>
	<Row>
		<Column>
			<TextInput placeholder="new epic area's full name" bind:value={newEpicAreaName} />
		</Column>
		<Autocomplete
			options={epics}
			selectDisplay="epic_name"
			bind:selectedOption={selectedEpic}
			placeholder="search epics"
		/>
		<Column>
			<DateTimePicker bind:value={startDate} />
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
					{ key: 'epic_area_name', value: "EPIC AREA'S NAME" },
					{ key: 'epic_name', value: "EPIC'S NAME" },
					{ key: 'is_active', value: 'IS ACTIVE' }
				]}
				rows={epicAreas}
				bind:selectedRowIds
				bind:updatedData
				{onUpdate}
				columnsToEdit={{
					epic_area_name: 'input',
					epic_name: {
						type: 'autocomplete',
						selectDisplay: 'epic_name',
						options: epics,
						placeholder: 'epic name'
					},
					is_active: 'toggle'
				}}
			/>
		</Column>
	</Row>
</Grid>
