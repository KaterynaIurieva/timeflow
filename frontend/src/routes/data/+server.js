import { env } from '$env/dynamic/public'


export const baseUrl = env.PUBLIC_SVELTEKIT_DEV_BASE_URL
/**
 * @param {any} timelogs
 */
async function getTimelogs(timelogs) {
    const response = await fetch(`${baseUrl}/api/timelogs/`, {
        method: 'GET',
        headers: { 'Content-type': 'application/json' }
    });
    timelogs = await response.json();
    return timelogs;
};
/**
 * @param {boolean} is_active
 */
async function getUsers(is_active) {
    let response
    if (is_active === true) {
        response = await fetch(`${baseUrl}/api/users/?is_active=${is_active}`, {
            method: 'GET',
            headers: { 'Content-type': 'application/json' }
        });
    } else {
        response = await fetch(`${baseUrl}/api/users/`, {
            method: 'GET',
            headers: { 'Content-type': 'application/json' }
        });
    }
    let users = await response.json()
    return users
};
async function getEpics() {
    const response = await fetch(`${baseUrl}/api/epics/`, {
        method: 'GET',
        headers: { 'Content-type': 'application/json' }
    });
    let epics = await response.json()
    return epics
};
async function getEpicAreas() {
    const response = await fetch(`${baseUrl}/api/epic_areas/`, {
        method: 'GET',
        headers: { 'Content-type': 'application/json' }
    });
    let epicAreas = await response.json()
    return epicAreas
};
/**
 * @param {any} capacities
 */
async function getCapacities(capacities) {
    const response = await fetch(`${baseUrl}/api/capacities/`, {
        method: 'GET',
        headers: { 'Content-type': 'application/json' }
    });
    capacities = await response.json()
    return capacities
};
async function getClients() {
    const response = await fetch(`${baseUrl}/api/clients/`, {
        method: 'GET',
        headers: { 'Content-type': 'application/json' }
    });
    let clients = await response.json()
    return clients
};

async function getSponsors() {
    const response = await fetch(`${baseUrl}/api/sponsors/`, {
        method: 'GET',
        headers: { 'Content-type': 'application/json' }
    });
    let sponsors = await response.json()
    return sponsors
};

async function getTeams() {
    const response = await fetch(`${baseUrl}/api/teams/`, {
        method: 'GET',
        headers: { 'Content-type': 'application/json' }
    });
    let teams = await response.json()
    return teams
};

async function getRoles() {
    const response = await fetch(`${baseUrl}/api/roles/`, {
        method: 'GET',
        headers: { 'Content-type': 'application/json' }
    });
    let roles = await response.json()
    return roles
};

async function getRate() {
    const response = await fetch(`${baseUrl}/api/rates/`, {
        method: 'GET',
        headers: { 'Content-type': 'application/json' }
    });
    let rate = await response.json()
    return rate
};
async function getForecasts() {
    const response = await fetch(`${baseUrl}/api/forecasts/`, {
        method: 'GET',
        headers: { 'Content-type': 'application/json' }
    });
    let forecasts = await response.json()
    return forecasts
};


export { getTimelogs, getUsers, getEpics, getEpicAreas, getCapacities, getClients, getSponsors, getTeams, getRoles, getRate, getForecasts }