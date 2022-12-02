<script lang="ts">
	import { onMount } from 'svelte';
	import { baseUrl } from '../data/+server.js';
	import { getForecasts, getEpics, getUsers } from '../data/+server.js';
	import EditableDatatable from '../../library/components/EditableDatatable.svelte';
	import Autocomplete from '../../library/components/autocomplete.svelte';
	import { clickOutside } from '/home/kateryna_iurieva/timeflow/frontend/src/clickOutside.js';
	import { Grid, Column, Row, Button, NumberInput } from '../../library/carbon/components';
	let forecasts = [{}];
	let users: any = [{}];
	let epics = [{}];
	let selectedRowIds: Array<number> = [];
	let selectedUser: object = {};
	let selectedEpic: object = {};
	let forecastDays: number = 0;
	let selectedMonth: string = '';
	let updatedData: Array<object> = [];

	function handleClickOutside(event) {
		updatedData = [];
		selectedRowIds = [];
	}
	onMount(async () => {
		users = await getUsers(true);
	});
	onMount(async () => {
		epics = await getEpics();
	});
	onMount(async () => {
		forecasts = await getForecasts();
	});
	async function onSubmit() {
		const res = await fetch(`${baseUrl}/api/forecasts/`, {
			method: 'POST',
			headers: { 'Content-type': 'application/json' },
			body: JSON.stringify({
				user_id: selectedUser.id,
				epic_id: selectedEpic.id,
				month: selectedMonth.slice(5),
				year: selectedMonth.slice(-7, -3),
				days: forecastDays,
				is_locked: false,
				created_at: Date.now(),
				updated_at: Date.now()
			})
		});
		forecasts = await getForecasts();
	}
	async function onUpdate() {
		const updateRes = await fetch(`${baseUrl}/api/forecasts/bulk_update`, {
			method: 'POST',
			headers: { 'Content-type': 'application/json' },
			body: JSON.stringify(updatedData)
		});
		forecasts = await getForecasts();
		updatedData = [];
		selectedRowIds = [];
	}

	async function onRemove() {
		async function DeleteApi(id: number) {
			const response = await fetch(`${baseUrl}/api/forecasts/?forecast_id=` + id, {
				method: 'DELETE',
				headers: {
					'Content-type': 'application/json'
				}
			});
			forecasts = await getForecasts();
		}
		selectedRowIds.map(DeleteApi);
	}
</script>

<Grid>
	<Row>
		<Column>
			<Autocomplete
				options={users}
				selectDisplay="full_name"
				bind:selectedOption={selectedUser}
				placeholder="select user"
			/>
		</Column>
		<Column>
			<Autocomplete
				options={epics}
				selectDisplay="epic_name"
				bind:selectedOption={selectedEpic}
				placeholder="search epic"
			/>
		</Column>
		<Column>
			<NumberInput bind:value={forecastDays} />
		</Column>

		<Column>
			<input class="month-picker" type="month" bind:value={selectedMonth} />
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
						{ key: 'full_name', value: 'USER' },
						{ key: 'epic_name', value: 'EPIC NAME' },
						{ key: 'year', value: 'YEAR' },
						{ key: 'month', value: 'MONTH' },
						{ key: 'forecast_days', value: 'DAYS' }
					]}
					rows={forecasts}
					bind:selectedRowIds
					bind:updatedData
					{onUpdate}
					{onRemove}
					columnsToEdit={{ forecast_days: 'number' }}
				/>
			</div>
		</Column>
	</Row>
</Grid>
