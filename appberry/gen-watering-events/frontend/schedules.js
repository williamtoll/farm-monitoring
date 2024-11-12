
import API_BASE_URL from './config.js';

document.addEventListener('DOMContentLoaded', async () => {
    const scheduleForm = document.getElementById('scheduleForm');
    const deviceSelect = document.getElementById('device');
    const scheduleTableBody = document.getElementById('scheduleTable').querySelector('tbody');
    let editScheduleId = null;

    // Load devices into the dropdown
    await loadDevices();

    // Load schedules into the table
    await loadSchedules();

    // Handle form submission
    scheduleForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const scheduleData = {
            device_id: deviceSelect.value,
            date: document.getElementById('date').value,
            start_time: document.getElementById('startTime').value,
            end_time: document.getElementById('endTime').value,
            duration: document.getElementById('duration').value,
        };

        if (editScheduleId) {
            await updateSchedule(editScheduleId, scheduleData);
        } else {
            await createSchedule(scheduleData);
        }

        // Clear the form and reload schedules
        resetForm();
        await loadSchedules();
    });

    // Load devices
    async function loadDevices() {
        try {
            const response = await fetch(`${API_BASE_URL}/devices`);
            const result = await response.json();
            console.log("result")
            console.dir(result)

            if (result) {
                deviceSelect.innerHTML = result
                    .map(device => `<option value="${device.id}">${device.name}</option>`)
                    .join('');
            } else {
                alert(`Error loading devices: ${result.message}`);
            }
        } catch (error) {
            alert(`Failed to load devices: ${error.message}`);
        }
    }

    // Load schedules
    async function loadSchedules() {
        try {
            const response = await fetch(`${API_BASE_URL}/schedules`);
            const result = await response.json();

            if (result.status === 'success') {
                scheduleTableBody.innerHTML = result.result
                    .map(schedule => `
                        <tr>
                            <td>${schedule.device_name}</td>
                            <td>${schedule.start}</td>
                            <td>${schedule.start}</td>
                            <td>${schedule.end}</td>
                            <td>${schedule.duration_minutes} min</td>
                            <td>${schedule.status}</td>

                            <td>
                                <button onclick="editSchedule(${schedule.id})">Edit</button>
                                <button onclick="deleteSchedule(${schedule.id})">Delete</button>
                            </td>
                        </tr>
                    `).join('');
            } else {
                alert(`Error loading schedules: ${result.message}`);
            }
        } catch (error) {
            alert(`Failed to load schedules: ${error.message}`);
        }
    }

    // Create a schedule
    async function createSchedule(scheduleData) {
        try {
            const response = await fetch(`${API_BASE_URL}/schedules`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(scheduleData),
            });
            const result = await response.json();
            if (result.status !== 'success') {
                alert(`Error: ${result.message}`);
            }
        } catch (error) {
            alert(`Failed to create schedule: ${error.message}`);
        }
    }

    // Update a schedule
    async function updateSchedule(id, scheduleData) {
        try {
            const response = await fetch(`${API_BASE_URL}/schedules/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(scheduleData),
            });
            const result = await response.json();
            if (result.status !== 'success') {
                alert(`Error: ${result.message}`);
            }
        } catch (error) {
            alert(`Failed to update schedule: ${error.message}`);
        }
    }

    // Delete a schedule
    window.deleteSchedule = async function (id) {
        try {
            const response = await fetch(`${API_BASE_URL}/schedules/${id}`, { method: 'DELETE' });
            const result = await response.json();
            if (result.status === 'success') {
                await loadSchedules();
            } else {
                alert(`Error: ${result.message}`);
            }
        } catch (error) {
            alert(`Failed to delete schedule: ${error.message}`);
        }
    };

    // Edit a schedule
    window.editSchedule = async function (id) {
        const schedule = await fetchScheduleById(id);
        if (schedule) {
            deviceSelect.value = schedule.device_id;
            document.getElementById('date').value = schedule.date;
            document.getElementById('start').value = schedule.start_time;
            document.getElementById('end').value = schedule.end_time;
            document.getElementById('duration_min').value = schedule.duration;
            document.getElementById('status').value = schedule.status;

            editScheduleId = id;
        }
    };

    async function fetchScheduleById(id) {
        try {
            const response = await fetch(`${API_BASE_URL}/schedules/${id}`);
            const result = await response.json();
            return result.status === 'success' ? result.result : null;
        } catch (error) {
            alert(`Failed to load schedule: ${error.message}`);
            return null;
        }
    }

    function resetForm() {
        scheduleForm.reset();
        editScheduleId = null;
    }
});
