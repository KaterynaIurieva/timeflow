<!-- update functionality not working yet! -->
<script lang="ts">
	import {
		DataTable,
		Toolbar,
		Button,
		Pagination,
		ToolbarBatchActions,
		ToolbarContent,
		ToolbarSearch
	} from '../carbon/components';
	import { Toggle, TextInput, NumberInput } from '../carbon/components';
	import Autocomplete from './autocomplete.svelte';
	import { TrashCan, UpdateNow } from '../carbon/icons';

	export let headers: Array<Object> = [];
	export let rows: any = [{}];
	export let selectedRowIds: Array<number> = [];
	export let onRemove: Function;
	export let onUpdate: Function;
	export let updatedData: { id: number; name: string }[] = [];
	export let columnsToEdit: Object = {};
	export let filteredRowIds: any = [];

	//@ts-ignore
	function updateData(event, event_row, event_cell, autocomplete: any = null) {
		let columnName: string = event_cell.cell.key;
		let cellValue = event_cell.cell.value;
		let rowId = event_row.row.id;
		let row = event_row.row;
		console.log('event', event);
		//@ts-ignore
		if (!(updatedData.filter((obj) => obj.id === rowId).length > 0)) {
			updatedData = [...updatedData, row];
		}
		let objIndex: any = updatedData.findIndex((obj) => obj.id === rowId);
		//@ts-ignore
		if (columnName === 'is_active') {
			updatedData[objIndex][columnName] = event.srcElement.checked;
		} else if (autocomplete) {
			updatedData[objIndex][columnName] = event[autocomplete.dataColumnName];
		} else {
			updatedData[objIndex][columnName] = event.srcElement.value;
		}
	}
	// if (selectedRowIds == ) {updatedData = []}
</script>

<DataTable
	sortable
	selectable
	bind:selectedRowIds
	{headers}
	pageSize={Pagination.pageSize}
	page={Pagination.page}
	{rows}
>
	<Toolbar>
		<ToolbarContent>
			<ToolbarSearch persistent shouldFilterRows bind:filteredRowIds />
		</ToolbarContent>
		<ToolbarBatchActions>
			{#if onRemove}
				<Button style="order:1;" icon={TrashCan} on:click={onRemove}>Remove</Button>
			{/if}
			{#if onUpdate}
				<Button style="order:1;" icon={UpdateNow} on:click={onUpdate}>Update</Button>
			{/if}
		</ToolbarBatchActions>
	</Toolbar>

	<svelte:fragment slot="cell" let:cell let:row let:rowIndex let:cellIndex>
		{#if selectedRowIds.includes(row.id)}
			{#if cell.key in columnsToEdit}
				{#each Object.entries(columnsToEdit) as [column, value]}
					{#if cell.key === column}
						{#if value === 'input'}
							<input
								type="text"
								class="month-picker"
								value={cell.value}
								on:blur={(event) => updateData(event, { row }, { cell })}
							/>
						{:else if value === 'datetime'}
							<input
								type="datetime-local"
								class="month-picker"
								value={cell.value}
								on:blur={(event) => updateData(event, { row }, { cell })}
							/>
						{:else if value === 'date'}
							<input
								type="date"
								class="month-picker"
								value={cell.value}
								on:blur={(event) => updateData(event, { row }, { cell })}
							/>
						{:else if value === 'number'}
							<input
								type="number"
								class="month-picker"
								value={cell.value}
								on:blur={(event) => updateData(event, { row }, { cell })}
							/>
						{:else if value === 'toggle'}
							<Toggle
								hideLabel
								size="sm"
								labelA="Inactive"
								labelB="Active"
								toggled={cell.value}
								on:change={(event) => updateData(event, { row }, { cell })}
							/>
						{:else if value.type === 'autocomplete'}
							<Autocomplete
								options={value.options}
								selectDisplay={value.selectDisplay}
								placeholder={value.placeholder}
								text={cell.value}
								onChange={(event) =>
									updateData(event, { row }, { cell }, { dataColumnName: value.selectDisplay })}
							/>
						{:else}
							{cell.value}
						{/if}
					{/if}
				{/each}
			{:else}
				{cell.value}
			{/if}
		{:else}
			{cell.value}
		{/if}
	</svelte:fragment>
</DataTable>
<Pagination
	bind:pageSize={Pagination.pageSize}
	bind:page={Pagination.page}
	totalItems={rows.length}
	pageSizeInputDisabled
/>
