import API_BASE_URL from "./config.js";

document.addEventListener("DOMContentLoaded", function () {
  let calendarEl = document.getElementById("calendar");

  let calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: window.innerWidth < 768 ? "listWeek" : "dayGridMonth",
    headerToolbar: {
      left: "prev,next today",
      center: "title",
      right:
        window.innerWidth < 768
          ? "listWeek"
          : "dayGridMonth,timeGridWeek,timeGridDay",
    },
    events: async function (fetchInfo, successCallback, failureCallback) {
      try {
        const response = await fetch(`${API_BASE_URL}/schedules`);
        const result = await response.json();

        if (result.status === "success") {
          const events = result.result.map((event) => ({
            id: event.schedule_id,
            title: `${event.device_name} (${event.duration_minutes} min)`,
            start: event.start,
            end: event.end,
          }));
          successCallback(events);
        } else {
          failureCallback(result.message);
        }
      } catch (error) {
        failureCallback(error.message);
      }
    },
    eventClick: function (info) {
      const eventId = info.event.id;

      if (confirm(`Are you sure you want to delete this schedule?`)) {
        deleteSchedule(eventId, info.event, calendar);
      }
    },
    height: "auto",
    nowIndicator: true,
    editable: true,
  });

  calendar.render();
});

async function deleteSchedule(scheduleId, event, calendar) {
  try {
    const response = await fetch(`${API_BASE_URL}/schedules/${scheduleId}`, {
      method: "DELETE",
    });

    const result = await response.json();

    if (result.status === "success") {
      alert("Schedule deleted successfully.");
      event.remove();
    } else {
      alert(`Error: ${result.message}`);
    }
  } catch (error) {
    alert(`Failed to delete schedule: ${error.message}`);
  }
}
