<script lang="ts">
	import 'carbon-components-svelte/css/white.css';
	import { onMount } from 'svelte';
	import { baseUrl } from '../data/+server.js';
	import {
		DataTable,
		Grid,
		Column,
		Row,
		Button,
		Pagination,
		Toolbar,
		ToolbarBatchActions,
		NumberInput
	} from '../../library/carbon/components';
	import { TrashCan } from '../../library/carbon/icons';
	import { getUsers, getCapacities } from '../data/+server.js';
	import Autocomplete from '../../library/components/autocomplete.svelte';
	import EditableDatatable from '../../library/components/EditableDatatable.svelte';

	let users: any[];
	let capacities = [{ id: '', last_name: '', first_name: '', year: '', month: '', days: '' }];
	let userId = '';
	let result: any = null;
	let selectedUser = { id: '' };
	let selectedRowIds: any = [];
	let selectedItemDisplay = '';
	let selectedItemValue = '';
	let capacityDays: number;
	let updatedData: [];
	let time = '';

	onMount(async () => {
		users = await getUsers(true);
	});
	onMount(async () => {
		capacities = await getCapacities(capacities);
	});

	async function onSubmit() {
		const res = await fetch(`${baseUrl}/api/capacities/`, {
			method: 'POST',
			headers: { 'Content-type': 'application/json' },
			body: JSON.stringify({
				user_id: selectedUser.id,
				days: capacityDays,
				month: time.slice(5, 8),
				year: time.slice(0, 4),
				created_at: Date.now(),
				updated_at: Date.now(),
				is_locked: false
			})
		});
		const json = await res.json();
		result = JSON.stringify(json);
		capacities = await getCapacities(capacities);
	}
	async function onUpdate() {
		const updateRes = await fetch(`${baseUrl}/api/capacities/bulk_update`, {
			method: 'POST',
			headers: { 'Content-type': 'application/json' },
			body: JSON.stringify(updatedData)
		});
		capacities = await getCapacities(capacities);
		updatedData = [];
		selectedRowIds = [];
	}
	async function onRemove() {
		async function DeleteApi(id: number) {
			const response = await fetch(`${baseUrl}/api/capacities/?capacity_id=` + id, {
				method: 'DELETE',
				headers: {
					'Content-type': 'application/json'
				},
				body: JSON.stringify({
					user_id: selectedUser.id,
					days: capacityDays,
					month: time.slice(5, 8),
					year: time.slice(0, 4),
					created_at: Date.now(),
					updated_at: Date.now(),
					is_locked: false
				})
			});
			capacities = await getCapacities(capacities);
		}
		selectedRowIds.map(DeleteApi);
	}

	async function handleSelect(selectedItem: any) {
		selectedUser = selectedItem;
	}
</script>

<Grid>
	<Row>
		<Column>
			<Autocomplete
				onChange={handleSelect}
				options={users}
				selectDisplay="username"
				placeholder="select user"
			/>
		</Column>
		<Column>
			<input class="month-picker" type="month" bind:value={time} />
		</Column>
		<Column>
			<input type="number" min="0" class="number-picker" bind:value={capacityDays} />
		</Column>
		<Column>
			<Button size="small" kind="primary" on:click={onSubmit}>Submit</Button>
		</Column>
	</Row>
	<Row>
		<Column>
			<EditableDatatable
				headers={[
					{ key: 'id', value: 'capacity ID' },
					{ key: 'full_name', value: 'USER' },
					{ key: 'year', value: 'YEAR' },
					{ key: 'month', value: 'MONTH' },
					{ key: 'days', value: 'CAPACITY DAYS' }
				]}
				rows={capacities}
				bind:selectedRowIds
				bind:updatedData
				{onUpdate}
				{onRemove}
				columnsToEdit={{
					days: 'number'
				}}
			/>
			<!-- <Toolbar>
				<ToolbarBatchActions>
					<Button icon={TrashCan} on:click={onRemove}>Remove</Button>
				</ToolbarBatchActions>
			</Toolbar>
			<Pagination bind:pageSize={Pagination.pageSize} bind:page={Pagination.page} /> -->
		</Column>
	</Row>
</Grid>
